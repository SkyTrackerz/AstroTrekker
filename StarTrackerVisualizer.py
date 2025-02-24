import vpython as vp
from math import radians, sin, cos
from StarTracker.IStarTracker import IStarTracker
from StarTracker.MockStarTracker import MockStarTracker

class StarTrackerVisualization:
    def __init__(self, star_tracker: IStarTracker):
        self.star_tracker = star_tracker
        self.scene = vp.canvas(title="Star Tracker Visualization", width=800, height=600, center=vp.vector(0, 0, 0),
                               background=vp.color.black)

        # Create celestial sphere
        self.celestial_sphere = vp.sphere(radius=100, texture=vp.textures.earth)

        # Create star tracker body
        self.tracker_body = vp.cylinder(axis=vp.vector(0, 1, 0), radius=0.5, length=2, color=vp.color.gray(0.7))

        # Create tracker camera (represented as a cone)
        self.tracker_camera = vp.cone(pos=vp.vector(0, 1, 0), axis=vp.vector(0, 1, 0), radius=0.3, color=vp.color.red)

        # Create astronomical body (e.g., a bright star)
        self.astro_body = vp.sphere(radius=0.2, color=vp.color.yellow, emissive=True)

        # POV camera
        self.pov_camera = vp.local_light(pos=vp.vector(0, 1, 0), color=vp.color.white)

        # Initialize POV scene
        self.pov_scene = vp.canvas(title="Star Tracker POV", width=400, height=400, center=vp.vector(0, 0, 0),
                                   background=vp.color.black)
        self.pov_stars = []
        self.create_random_stars(100)  # Create 100 random stars for POV view

    def create_random_stars(self, num_stars):
        for _ in range(num_stars):
            star = vp.sphere(canvas=self.pov_scene, radius=0.01, color=vp.color.white, emissive=True)
            star.random_pos = vp.vector.random()  # Store random position
            self.pov_stars.append(star)

    def update_visualization(self):
        altitude, azimuth, spin = self.star_tracker.get_current_pos()

        # Update tracker orientation
        self.tracker_body.axis = vp.vector(sin(radians(azimuth)) * cos(radians(altitude)),
                                           sin(radians(altitude)),
                                           cos(radians(azimuth)) * cos(radians(altitude)))
        self.tracker_camera.axis = self.tracker_body.axis
        self.tracker_camera.pos = self.tracker_body.axis

        # Update POV camera
        self.pov_camera.pos = self.tracker_body.axis

        # Rotate celestial sphere (simulating Earth's rotation)
        self.celestial_sphere.rotate(angle=radians(spin), axis=vp.vector(0, 1, 0))

        # Update POV stars
        for star in self.pov_stars:
            rotated_pos = star.random_pos.rotate(angle=radians(-altitude), axis=vp.vector(1, 0, 0))
            rotated_pos = rotated_pos.rotate(angle=radians(-azimuth), axis=vp.vector(0, 1, 0))
            rotated_pos = rotated_pos.rotate(angle=radians(-spin), axis=vp.vector(0, 0, 1))
            star.pos = rotated_pos * 10  # Scale the position to make stars visible

    def set_astro_body_position(self, alt, az):
        self.astro_body.pos = vp.vector(sin(radians(az)) * cos(radians(alt)),
                                        sin(radians(alt)),
                                        cos(radians(az)) * cos(radians(alt))) * 99  # Just inside celestial sphere

    def run(self):
        while True:
            vp.rate(30)  # Update 30 times per second
            self.update_visualization()


# Usage example:
if __name__ == "__main__":


    mock_tracker = MockStarTracker()
    vis = StarTrackerVisualization(mock_tracker)

    # Set position of an astronomical body (e.g., a bright star)
    vis.set_astro_body_position(alt=45, az=180)

    # Simulate some movements
    mock_tracker.go_to_absolute(altitude=30, azimuth=45, spin=0)
    vis.run()