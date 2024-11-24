import tkinter as tk
import os
from PIL import Image, ImageTk
import pandas as pd
import PIL

currentIndex = 1
maxColumn = 5
path = './pokemon_data/content/pokemon_images/'
csvPath = "./pokemons2.csv"
mediumFont = 15

df = pd.read_csv(csvPath)
column_name = 'name'
pNames = df[column_name].tolist()

def count_files_in_directory(directory):
    # Get a list of all files and directories in the specified directory
    files = os.listdir(directory)
    # Count only files, ignoring directories
    file_count = sum(1 for f in files if os.path.isfile(os.path.join(directory, f)))
    return file_count

def showNext():
	global currentIndex, maxId
	if currentIndex == maxId:
		currentIndex = 1
	else:
		currentIndex += 1
	updateItem()

def showPrevious():
	global currentIndex, maxId
	if currentIndex == 1:
		currentIndex = maxId
	else:
		currentIndex -= 1
	updateItem()

def searchItem():
	global userInput, currentIndex, maxId
	user_input = userInput.get()
	if user_input.isdigit():
		index = int( user_input )
		if index < maxId and index > 0:
			currentIndex = index
		else:
			displayErr("Invalid Id !!!")
			return
	else:
		searchItemByName(user_input)
		return
	updateItem()

def searchItemByName(user_input):
	global currentIndex, pNames, userInput
	user_input = user_input.lower()
	#print( pNames )
	if  user_input in pNames:
		index = pNames.index(user_input)
		currentIndex = index + 1
	else:
		displayErr("Invalid pokemon !!!")
		return
	updateItem()

def updateItem():
	global currentIndex, path, labelImage, pNames, labelType

	imagePath = path
	if currentIndex < 10:
		imagePath += "00" + str( currentIndex ) + ".png"
	elif currentIndex < 100:
		imagePath += "0" + str( currentIndex ) + ".png"
	else:
		imagePath += str( currentIndex ) + ".png" 
	# print( imagePath)
	image = Image.open(imagePath)
	resized_photo = ImageTk.PhotoImage(image.resize((300, 300), PIL.Image.Resampling.LANCZOS))
	labelImage.config(image=resized_photo)
	labelImage.image = resized_photo

	labelName.config(text="#" + str( currentIndex ) + "  " + pNames[currentIndex - 1].capitalize())
	
	row_data = df.iloc[currentIndex-1].tolist()
	if pd.isna( row_data[6] ):
		labelType.config(text=row_data[5].capitalize())
	else:
		labelType.config(text=row_data[5].capitalize() + "	" + row_data[6].capitalize() )
	
	labelWeightHeight.config(text=str( row_data[14]/10 ) + "m      " + str( row_data[15]/10 ) + " kg" )
	labelPower.config(text="HP/Atk/Def - " + str(row_data[7]) + "/" + str(row_data[8]) + "/"  + str(row_data[9]) )
	labelSpPower.config(text="SpAtk/SpDef - " + str(row_data[10]) + "/" + str(row_data[11]) )
	labelSpeed.config(text="Speed - " + str(row_data[12]) )
	labelTotal.config(text="Overall - " + str(row_data[13]) )
	labelAbilities.config(text="Abilities - " + str( row_data[16] ).capitalize() )
	labelDescription.config(text=str( row_data[17] ) )

	#print( currentIndex )

	labelErr.config(text="")
	return

def displayErr(errMsg):
	labelErr.config(text=errMsg)


# Specify the directory path
directory_path = path  # Change this to your directory
maxId = count_files_in_directory(directory_path)

root = tk.Tk()
root.title("Grid of Buttons")

root.columnconfigure(1, minsize=100)
root.columnconfigure(2, minsize=100)
root.columnconfigure(3, minsize=100)
root.columnconfigure(4, minsize=100)
root.columnconfigure(5, minsize=100)

currentRow = 0

buttonPrevious = tk.Button(root, text="Previous", command=lambda : showPrevious())
buttonPrevious.grid(row=currentRow, column=0, columnspan=1, sticky='w')
buttonNext = tk.Button(root, text="Next", command=lambda : showNext())
buttonNext.grid(row=currentRow, column=maxColumn, columnspan=1, sticky='e')

currentRow += 1
labelUserInput = tk.Label(root, text="Enter Pokemon name or Id", font=("Arial", 10), fg="blue")
labelUserInput.grid(row=currentRow, column=0, columnspan=1, sticky='w')
userInput = tk.Entry(root, width=30)
userInput.grid(row=currentRow, column=2, columnspan=2, sticky='w')
buttonSearch = tk.Button(root, text="Search", command=lambda : searchItem())
buttonSearch.grid(row=currentRow, column=maxColumn, columnspan=1, sticky='e')

currentRow += 1
labelErr = tk.Label(root, text="", font=("Arial", 10), fg="red")
labelErr.grid(row=currentRow, column=0, columnspan=maxColumn)

currentRow += 1
canvas = tk.Canvas(root, width=500, height=10)
canvas.grid(row=currentRow, column=0, columnspan=maxColumn)
canvas.create_line(1, 1, 1000, 1, width=2)  # (x1, y1, x2, y2)

currentRow += 1
labelName = tk.Label(root, text="", font=("Arial", 20))
labelName.grid(row=currentRow, column=0, columnspan=maxColumn+1, rowspan=1, sticky='ew')

currentRow += 1
labelImage = tk.Label(root, image="")
labelImage.grid(row=currentRow, column=0, columnspan=3, rowspan=6, sticky='w')

labelType = tk.Label(root, font=("Arial", mediumFont))
labelType.grid(row=currentRow, column=3, columnspan=3, rowspan=1, sticky='w')

currentRow += 1
labelWeightHeight = tk.Label(root, text="", font=("Arial", mediumFont))
labelWeightHeight.grid(row=currentRow, column=3, columnspan=3, rowspan=1, sticky='w')

currentRow += 1
labelPower = tk.Label(root, text="", font=("Arial", mediumFont))
labelPower.grid(row=currentRow, column=3, columnspan=3, rowspan=1, sticky='w')

currentRow += 1
labelSpPower = tk.Label(root, text="", font=("Arial", mediumFont))
labelSpPower.grid(row=currentRow, column=3, columnspan=3, rowspan=1, sticky='w')

currentRow += 1
labelSpeed = tk.Label(root, text="", font=("Arial", mediumFont))
labelSpeed.grid(row=currentRow, column=3, columnspan=3, rowspan=1, sticky='w')

currentRow += 1
labelTotal = tk.Label(root, text="", font=("Arial", mediumFont))
labelTotal.grid(row=currentRow, column=3, columnspan=3, rowspan=1, sticky='w')

currentRow += 3
labelAbilities = tk.Label(root, text="", font=("Arial", mediumFont))
labelAbilities.grid(row=currentRow, column=0, columnspan=maxColumn+1, rowspan=1, sticky='ew')

currentRow += 1
labelDescription = tk.Label(root, text="", font=("Arial", mediumFont), wraplength= 600)
labelDescription.grid(row=currentRow, column=0, columnspan=maxColumn+1, rowspan=1, sticky='ew')

updateItem()

root.mainloop()
