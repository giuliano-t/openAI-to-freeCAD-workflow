import FreeCAD as App
import Part

# Create a new document
doc = App.newDocument("EllipticalSections")

# Function to create an ellipse
def create_ellipse(center, major_radius, minor_radius, name):
    try:
        # Validate radii
        if major_radius <= 0 or minor_radius <= 0:
            raise ValueError(f"Invalid radii: major_radius={major_radius}, minor_radius={minor_radius}. Both must be positive.")

        # Ensure minor radius is not greater than major radius
        if minor_radius > major_radius:
            raise ValueError(f"Invalid dimensions: minor_radius ({minor_radius}) cannot be greater than major_radius ({major_radius}).")

        # Create the ellipse geometry
        ellipse = Part.Ellipse()
        ellipse.MajorRadius = major_radius
        ellipse.MinorRadius = minor_radius

        # Create the ellipse shape and convert to wire
        ellipse_shape = ellipse.toShape()
        wire = Part.Wire(ellipse_shape)

        # Add the wire to the document and return it as an object
        Part.show(wire, name)
        part_obj = doc.getObject(name)
        
        if part_obj:
            # Set placement
            part_obj.Placement = App.Placement(center, App.Rotation(App.Vector(0, 0, 1), 0))
            print(f"Successfully created {name}")
            return part_obj
        else:
            print(f"Error: Failed to add {name} to the document.")
            return None
    except Exception as e:
        print(f"Error creating ellipse {name}: {e}")
        return None

# Function to set the color of an object
def set_color(obj, color):
    try:
        if obj:
            viewObject = obj.ViewObject
            viewObject.ShapeColor = color
            print(f"Color set to {color} for {obj.Name}")
        else:
            print("Error: Object is None, cannot set color.")
    except Exception as e:
        print(f"Error setting color: {e}")

# Create the first ellipse on the XY plane
center1 = App.Vector(0, 0, 0)  # Center at origin
major_radius1 = 40 / 2  # Major axis divided by 2
minor_radius1 = 13 / 2  # Adjusted to ensure minor_radius < major_radius
ellipse1_obj = create_ellipse(center1, major_radius1, minor_radius1, "Ellipse1")

# Create the second ellipse on a plane parallel to XY and 30 cm above
center2 = App.Vector(0, 0, 33)  # Center at z = 30 cm
major_radius2 = 28 / 2  # Major axis divided by 2
minor_radius2 = 13 / 2  # Minor axis divided by 2
ellipse2_obj = create_ellipse(center2, major_radius2, minor_radius2, "Ellipse2")

# Check if both ellipses are created successfully
if ellipse1_obj and ellipse2_obj:
    try:
        # Create loft
        loft = doc.addObject("Part::Loft", "Loft")
        loft.Sections = [ellipse1_obj, ellipse2_obj]  # Pass document objects
        loft.Solid = False  # Ensure top and bottom sections remain open
        loft.Ruled = False
        loft.Closed = False

        # Set color for the loft
        set_color(loft, (1.0, 1.0, 0.0))  # Yellow color

        # Recompute the document to reflect changes
        doc.recompute()
        print("Elliptical sections and loft created successfully with open ends!")

        # Create isometric view
        Gui.activeDocument().activeView().viewIsometric()
        Gui.SendMsgToActiveView("ViewFit")
        print("Isometric view set and zoomed to fit.")
    except Exception as e:
        print(f"Error creating loft: {e}")
else:
    print("Error: One or both ellipses could not be created.")

# Create the third ellipse on the XY plane
center3 = App.Vector(0, 0, 0)  # Center at origin
major_radius3 = 19 / 2  # Major axis divided by 2
minor_radius3 = 9 / 2  # Minor axis divided by 2
ellipse3_obj = create_ellipse(center3, major_radius3, minor_radius3, "Ellipse3")

# Create the fourth ellipse on a plane 22 cm below the XY plane
center4 = App.Vector(0, 0, -22)  # Center at z = -22 cm
major_radius4 = 14 / 2  # Major axis divided by 2
minor_radius4 = 9 / 2  # Minor axis divided by 2
ellipse4_obj = create_ellipse(center4, major_radius4, minor_radius4, "Ellipse4")

# Check if both ellipses are created successfully
if ellipse3_obj and ellipse4_obj:
    try:
        # Create loft
        loft2 = doc.addObject("Part::Loft", "Loft2")
        loft2.Sections = [ellipse3_obj, ellipse4_obj]  # Pass document objects
        loft2.Solid = False  # Ensure top and bottom sections remain open
        loft2.Ruled = False
        loft2.Closed = False

        # Set color for the loft
        set_color(loft2, (1.0, 1.0, 0.0))  # Yellow color

        # Recompute the document to reflect changes
        doc.recompute()
        print("Elliptical sections (Ellipse3 and Ellipse4) and loft created successfully with open ends!")
    except Exception as e:
        print(f"Error creating loft: {e}")
else:
    print("Error: One or both ellipses could not be created.")
