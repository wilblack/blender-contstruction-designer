# blender-contstruction-designer

https://github.com/wilblack/blender-contstruction-designer


# Create venv

python3 -m venv blender_env
source blender_env/bin/activate


# Starting Blender

## This starts Blender 2.79
cd /Applications/Blender
./blender.app/Contents/MacOS/blender

/Applications/Blender/blender.app/Contents/MacOS/blender mtb_track.blend

I set and alias in my bashrc to the blender command, now just use `blender`

## Start with blender file
blender mtb_track.blend

## Start Blender and run  a script.
blender foo.blend --python pioneer_trail/set-up.py

/Applications/Blender/blender.app/Contents/MacOS/blender foo.blend --python pioneer_trail/set-up.py

## Resources

Blender Command Line

https://docs.blender.org/manual/en/latest/render/workflows/command_line.html
