"""Setup script for beerpong."""
import setuptools

if __name__ == "__main__":
    setuptools.setup(
        package_data={
            "beerpong": ["py.typed"],
        },
    )
