import FreeCAD as App
import Part
import math
import os

# Document
doc = App.newDocument("LPTBlade")

# Trapezoidal body parameters
base_width = 40
top_width = 20
height = 30
extrusion_length = 50

# Create trapezoidal face
def create_trapezoidal_profile(base_width, top_width, height):
    points = [
        App.Vector(-base_width / 2, 0, 0),
        App.Vector(base_width / 2, 0, 0),
        App.Vector(top_width / 2, height, 0),
        App.Vector(-top_width / 2, height, 0),
    ]
    wire = Part.makePolygon(points + [points[0]])
    return Part.Face(wire)

trapezoidal_face = create_trapezoidal_profile(base_width, top_width, height)
extruded_geometry = trapezoidal_face.extrude(App.Vector(0, 0, extrusion_length))

# Compute slope and intercept for inclined face
slope = height / (base_width / 2 - top_width / 2)
intercept = height - slope * (-top_width / 2)

# Add square cuts on inclined face
def create_square_on_tilted_face(x_translation):
    square_side = 3.5
    square_points = [
        App.Vector(0, 0, 0),
        App.Vector(square_side, 0, 0),
        App.Vector(square_side, -square_side, 0),
        App.Vector(0, -square_side, 0),
    ]
    square_wire = Part.makePolygon(square_points + [square_points[0]])
    square_face = Part.Face(square_wire)
    tilt_angle = math.degrees(math.atan(slope))
    square_face = square_face.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), tilt_angle)
    y_translation = slope * x_translation + intercept + 0.01
    square_face = square_face.translate(App.Vector(x_translation, y_translation, 0))
    return square_face.extrude(App.Vector(0, 0, extrusion_length))

# Generate and cut square extrusions
def map_top_percentage_to_bottom_x(percent, base_width, top_width):
    return top_width / 2 + percent * (base_width / 2 - top_width / 2)

percentages = [0.8, 0.55, 0.3]
cuts = [create_square_on_tilted_face(-map_top_percentage_to_bottom_x(p, base_width, top_width)) for p in percentages]

for cut in cuts:
    extruded_geometry = extruded_geometry.cut(cut)

# Mirror and cut the mirrored squares
mirrors = [cut.mirror(App.Vector(0, 0, 0), App.Vector(1, 0, 0)) for cut in cuts]
for cut in mirrors:
    extruded_geometry = extruded_geometry.cut(cut)

# Optional fillets
z_edges = [e for e in extruded_geometry.Edges if isinstance(e.Curve, Part.Line) and e.Curve.Direction.isParallel(App.Vector(0, 0, 1), 0.01)]
try:
    extruded_geometry = extruded_geometry.makeFillet(1.0, z_edges)
except Part.OCCError:
    pass

# Rotate to XY alignment
extruded_geometry = extruded_geometry.rotate(App.Vector(0, 0, 0), App.Vector(1, 0, 0), -90)

# Add rectangular protrusions on front
def add_front_feature(shape, z_start, z_thickness, rect_x=None, rect_y=None):
    if rect_x is None:
        rect_x = 0.5 * base_width
    if rect_y is None:
        rect_y = 0.8 * extrusion_length

    rect_center_y = extrusion_length / 2
    points = [
        App.Vector(-rect_x / 2, rect_center_y - rect_y / 2, z_start),
        App.Vector(rect_x / 2, rect_center_y - rect_y / 2, z_start),
        App.Vector(rect_x / 2, rect_center_y + rect_y / 2, z_start),
        App.Vector(-rect_x / 2, rect_center_y + rect_y / 2, z_start),
    ]
    wire = Part.makePolygon(points + [points[0]])
    face = Part.Face(wire)
    extrusion = face.extrude(App.Vector(0, 0, z_thickness))
    return shape.fuse(extrusion)


# Lower flange (same as before)
extruded_geometry = add_front_feature(extruded_geometry, 0, 10, rect_x=base_width*0.5, rect_y=extrusion_length*0.7)

# Upper flange (custom size: base_width x extrusion_length)
extruded_geometry = add_front_feature(extruded_geometry, 10, 5, rect_x=base_width, rect_y=extrusion_length)


Part.show(extruded_geometry)

# Find top face center
def get_top_face_and_center(shape):
    top_face = None
    max_z = float('-inf')
    top_center = None
    for face in shape.Faces:
        center = face.CenterOfMass
        if center.z > max_z:
            top_face = face
            max_z = center.z
            top_center = (center.x, center.y, center.z)
    return top_face, top_center

# NACA 0012 airfoil generator
def naca0012_points(chord, thickness_factor=5.0, num_points=100):
    points = []
    for i in range(num_points):
        x = chord * i / (num_points - 1) - chord / 2
        xi = max(x / chord + 0.5, 0.0)
        thickness = thickness_factor * 0.12 * chord * (
            0.2969 * math.sqrt(xi) - 0.1260 * xi - 0.3516 * xi**2 + 0.2843 * xi**3 - 0.1036 * xi**4
        )
        points.append((x, thickness))
        if i > 0:
            points.insert(0, (x, -thickness))
    return points

# Loft a twisted blade
def create_twisted_blade(base_center, chord, height, twist_angle, taper_ratio=0.7, thickness_factor=5.0, num_sections=10):
    sections = []
    twist_per_section = math.radians(twist_angle) / (num_sections - 1)
    for i in range(num_sections):
        z = base_center[2] + i * height / (num_sections - 1)
        twist = twist_per_section * i
        current_chord = chord * 0.75 * (1 - i / (num_sections - 1) * (1 - taper_ratio))
        airfoil = naca0012_points(current_chord, thickness_factor)
        transformed = []
        for p in airfoil:
            x_rot = p[0] * math.cos(twist) - p[1] * math.sin(twist)
            y_rot = p[0] * math.sin(twist) + p[1] * math.cos(twist)
            transformed.append(App.Vector(base_center[0] + x_rot, base_center[1] + y_rot, z))
        wire = Part.makePolygon(transformed + [transformed[0]])
        face = Part.Face(wire)
        sections.append(face)
    return Part.makeLoft(sections, True)

# Generate and add blade
_, top_center = get_top_face_and_center(extruded_geometry)
blade = create_twisted_blade(top_center, chord=50, height=160, twist_angle=45, taper_ratio=0.7, thickness_factor=5)

# Rotate 90 degrees around Z-axis
blade = blade.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), 90)

# Align blade base with top face center
blade_center = blade.BoundBox.Center
blade_bottom_z = blade.BoundBox.ZMin
translation_vector = App.Vector(
    top_center[0] - blade_center.x,
    top_center[1] - blade_center.y,
    top_center[2] - blade_bottom_z
)
blade = blade.translate(translation_vector)

# Add blade to document
Part.show(blade)

# Final doc settings
doc.recompute()
if hasattr(App.Gui, 'activeDocument'):
    App.Gui.activeDocument().activeView().viewIsometric()
    App.Gui.SendMsgToActiveView("ViewFit")

# Save
output_path = os.path.expanduser("~/LPT_Blade.FCStd")
doc.saveAs(output_path)
print(f"Saved at: {output_path}")
