#Your PI says: "Hey we have a collaborator who has fallen off the face of the earth. 
#We did a cool brain study and all that's left is the data analysis. I remember you 
# took that Python class, so you're a data analysis expert, right? Also if you 
#analyze these data you can graduate early."

#Your PI tells you the study was looking at brain responses when participants 
#hear correct and incorrect grammar. You do a little bit of research and decide 
#that you're going to analyze event-related potentials (ERPs).

#Your overall goal is to plot ERPs from all participants individually and an 
#overall average; ERPs should be reactions to (1) syntatically-acceptable sentences vs 
#(2) sentences with syntax errors. You decide for now you'll just analyze the 
#Australian English sentences. Hint: Start with plotting data from the Cz electrode,
#from one participant.

 

#For this assignment, do the following:

#Create a github account
#Fork Dr. Cler's repository: https://github.com/gabecler/SPHSC525_2024 Links to an external site.
#Use ChatGPT to get started. Commit the first try with ChatGPT to your repository. 
#Continue to commit periodically when you have a working version.

#When you are finished, submit to me:

#Link to your (public) repository with your final code
#A ~1 page summary of your results:
    #Plot of ERP from Cz for one participant, average of sentences without errors 
    #and average of sentences with errors. X-axis should be time and y-axis amplitude. 
    #Negative amplitude on y-axis can be down or up (EEG convention), but should be marked. 
    #X-axis should have 0 marked as onset of error.
    #Plot of average ERP from Cz for ALL participants, average of sentences without 
    #errors and average of sentences with errors. 
    
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import scipy
import mne
import pandas
import os


# Specify the directory you want to list
directory_path = '/Users/ariel/Desktop/Spring24/525/ERPlab/SS01'

# List all files in the specified directory
files_in_directory = os.listdir(directory_path)
print(files_in_directory)

# Loading in the EEG data

# Assuming 'SS01-SR-02082016.cnt' is your raw EEG file.
file_path = '/Users/ariel/Desktop/Spring24/525/ERPlab/SS01/SS01-SR-02082016-cnt.cnt'

raw = mne.io.read_raw_cnt(file_path, preload=True)
print(raw.info)  # To see information about the recording and available channels


raw = mne.io.read_raw_cnt(file_path, eog='auto', preload=True, verbose=None)

# Now you can access the data for the Cz electrode
cz_data = raw.pick_channels(['Cz'])

print(cz_data)










# when exploring the other files
# Examining each file in SS01

dap_file_path = '/Users/ariel/Desktop/Spring24/525/ERPlab/SS01/SS01-SR-02082016-cnt.dap'

# Attempt to open the .dap file and read its content as text
try:
    with open(dap_file_path, 'r') as file:
        dap_content = file.read()
        print(dap_content)
except Exception as e:
    print(f"An error occurred while reading .dap file: {e}")


rs3_file_path = '/Users/ariel/Desktop/Spring24/525/ERPlab/SS01/SS01-SR-02082016-cnt.rs3'

# Attempt to open the .rs3 file and read its content as text
try:
    with open(rs3_file_path, 'r') as file:
        rs3_content = file.read()
        print(rs3_content)
except Exception as e:
    print(f"An error occurred while reading .rs3 file: {e}")

rs3_second_file_path = '/Users/ariel/Desktop/Spring24/525/ERPlab/SS01/SS01-SR-02082016.rs3'

# Attempt to open the second .rs3 file and read its content as text
try:
    with open(rs3_second_file_path, 'r') as file:
        rs3_second_content = file.read()
        print(rs3_second_content)
except Exception as e:
    print(f"An error occurred while reading second .rs3 file: {e}")



import numpy as np

# Define the path to your .dat file
dat_file_path = '/Users/ariel/Desktop/Spring24/525/ERPlab/SS01/SS01-SR-02082016.dat'

# Define a function to read chunks of the file
def read_chunks(filepath, chunk_size=1024):
    with open(filepath, 'rb') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            yield chunk

# Read the first few chunks of the .dat file and attempt to interpret the binary data
for chunk in read_chunks(dat_file_path, chunk_size=1024):
    # Interpret the binary data as integers
    chunk_data = np.frombuffer(chunk, dtype=np.int32)
    print(chunk_data)
    break  # Remove this to read more chunks














# Plotting the whole EEG for Cz electrode.
# Load the raw data
raw = mne.io.read_raw_cnt(file_path, preload=True)

# Pick the Cz channel by name
picks = mne.pick_channels(raw.info['ch_names'], include=['Cz'])

# Plot the continuous data for the Cz electrode
raw.plot(picks=picks, duration=5, start=5)  # Plots 5 seconds of data starting at 5 seconds

#No stim channels found, but the raw object has annotations. 
#Consider using mne.events_from_annotations to convert these to events.

# Convert annotations to events
events, event_id = mne.events_from_annotations(raw)

# Now print the unique event IDs to see what we have
unique_event_ids = np.unique(events[:, 2])  # The event IDs are in the third column
print(f"Unique event IDs found: {unique_event_ids}")



# Get the events and event_id mapping from annotations
events, event_id = mne.events_from_annotations(raw)

# Double check if the event IDs 203 and 207 are present in the event_id dictionary
if '203' in event_id and '207' in event_id:
    # Create epochs around these specific events
    epochs = mne.Epochs(raw, events, event_id={'congruent': event_id['203'], 'incongruent': event_id['207']},
                        tmin=-0.2, tmax=0.8, preload=True, baseline=(None, 0), picks='Cz')
else:
    print("The event IDs 203 and 207 are not found in the annotations.")

# Average the epochs to get ERPs
evoked_congruent = epochs['congruent'].average()
evoked_incongruent = epochs['incongruent'].average()

# Plot ERPs
fig, ax = plt.subplots(figsize=(10, 7))

# Plot the averaged ERP for congruent condition in green
evoked_congruent.plot(axes=ax, time_unit='s', show=False)
ax.lines[0].set_label('Congruent')  # Set label for the legend

# Plot the averaged ERP for incongruent condition
evoked_incongruent.plot(axes=ax, time_unit='s', show=False)
ax.lines[1].set_label('Incongruent')  # Set label for the legend

ax.axvline(0, linestyle='--', color='black', linewidth=2)  # Marking the event onset
ax.legend()  # Add legend
plt.show()










