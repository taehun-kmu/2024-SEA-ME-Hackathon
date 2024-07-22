from setuptools import setup

setup(
    name='rim_track2',
    version='0.0.1',
    packages=['rim_track2'],
    package_dir={'': 'src'},
    install_requires=[
        'opencv-python',
        'numpy',
    ],
    entry_points={
        'console_scripts': [
            'line_detection_node = rim_track2.line_detection_node:main',
            'obstacle_detection_node = rim_track2.obstacle_detection_node:main',
            'signal_detection_node = rim_track2.signal_detection_node:main',
            'arduino_interface = rim_track2.arduino_interface:main',
            'camera_calibration = rim_track2.camera_calibration:main',
        ],
    },
)

