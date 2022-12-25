import subprocess
import sys
import time

# Set up the FFmpeg command
command = ['ffmpeg', '-i', 'C:\\Users\\Blunt\\Desktop\\New folder\\input.webm', '-c:v', 'libx264', '-crf', '28', '-pix_fmt', 'yuv420p', 'C:\\Users\\Blunt\\Desktop\\New folder\\output\\output.mp4', ]

# Start the FFmpeg process
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

# Initialize variables for progress tracking
total_size = 0
current_size = 0
start_time = time.time()

# Print the progress bar
while True:
    # Read a line of output from the process
    line = process.stdout.readline().decode('utf-8').strip()

    # If the process has finished, break out of the loop
    if line == '' and process.poll() is not None:
        break

    # Parse the progress information from the line
    if 'size=' in line:
        # Extract the total size and current size from the line
        total_size = int(line.split('size=')[1].split('kB')[0])
        current_size = int(line.split('time=')[0].split('size=')[1].split('kB')[0])

        # Calculate the progress as a percentage
        progress = current_size / total_size * 100

        # Calculate the elapsed time and estimated remaining time
        elapsed_time = time.time() - start_time
        remaining_time = elapsed_time / progress * (100 - progress)

        # Print the progress bar
        sys.stdout.write('\r[{}{}] {:.2f}% ({:.2f}/{:.2f} MB) ETA: {:.2f}s'.format('#' * int(progress // 2), ' ' * int(50 - progress // 2), progress, current_size / 1024, total_size / 1024, remaining_time))
        sys.stdout.flush()

# Print a newline after the progress bar
print()

# Wait for the process to finish
process.wait()

# Check the exit code
if process.returncode == 0:
    print('Transcoding successful!')
else:
    print('Transcoding failed with exit code {}'.format(process.returncode))