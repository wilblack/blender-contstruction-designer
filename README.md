# blender-contstruction-designer

https://github.com/wilblack/blender-contstruction-designer


# Create venv

python3 -m venv blender_env
source blender_env/bin/activate


# Starting Blender

## This starts Blender 2.79

/Applications/Blender/blender.app/Contents/MacOS/blender mtb_track.blend

I set an alias in my bashrc to the blender command, now just use `blender`

## Start Blender and run  a script.
cd /Users/wilblack/Projects/blender/blender-contstruction-designer
blender --python pioneer_trail/set-up.py

/Applications/Blender/blender.app/Contents/MacOS/blender foo.blend --python pioneer_trail/set-up.py

## Resources

Blender Command Line

https://docs.blender.org/manual/en/latest/render/workflows/command_line.html
