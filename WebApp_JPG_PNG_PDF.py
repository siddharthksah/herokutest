# importing the necessary packages
import fitz
import base64
import re
import time
from cv2 import *
import pandas as pd
import pytesseract
import streamlit as st
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = './.apt/usr/bin/tesseract'


uploaded_file1 = st.file_uploader("Choose the front image", type=['jpg', 'png', 'pdf'], key=1)

if uploaded_file1 is not None:
    # st.write(uploaded_file1)
    file_name_1 = uploaded_file1.name
    extension1 = file_name_1.split(".")[1]
    # st.write(extension1)
    file_name_1 = uploaded_file1.name
    extension1 = file_name_1.split(".")[1]
    # st.write(extension1)
    if extension1 == "pdf":
        # front_image = Image.open(uploaded_file1)
        # st.image(front_image, caption='Uploaded Front Image', use_column_width=True)
        doc = fitz.open(stream=uploaded_file1.read(), filetype="pdf")
        for i in range(len(doc)):
            for img in doc.getPageImageList(i):
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                if pix.n < 5:  # this is GRAY or RGB
                    # pix.writePNG("./data/temp/p%s-%s.png" % (i, xref))
                    pix.writePNG("./data/temp/front_temp.png")
                else:  # CMYK: convert to RGB first
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)
                    # pix1.writePNG("./data/temp/p%s-%s.png" % (i, xref))
                    pix.writePNG("./data/temp/front_temp.png")
                    pix1 = None
                pix = None
        st.image("./data/temp/front_temp.png", use_column_width=True)

    elif extension1 == "png":

        front_image = Image.open(uploaded_file1)
        st.image(front_image, caption='Uploaded Front Image', use_column_width=True)

    elif extension1 == "jpg":
        #SHOW IMAGE IF JPG FORMAT
        front_image = Image.open(uploaded_file1)
        st.image(front_image, caption='Uploaded Front Image', use_column_width=True)

    else:
        st.write("Please upload .JPG, .PNG OR .PDF format file only!")

uploaded_file2 = st.file_uploader("Choose the back image", type=['jpg', 'png', 'pdf'], key=2)

if uploaded_file2 is not None:
    # st.write(uploaded_file2)
    file_name_2 = uploaded_file2.name
    extension2 = file_name_2.split(".")[1]
    # st.write(extension1)
    file_name_2 = uploaded_file2.name
    extension2 = file_name_2.split(".")[1]
    # st.write(extension1)
    if extension2 == "pdf":
        # front_image = Image.open(uploaded_file1)
        # st.image(front_image, caption='Uploaded Front Image', use_column_width=True)
        doc = fitz.open(stream=uploaded_file2.read(), filetype="pdf")
        for i in range(len(doc)):
            for img in doc.getPageImageList(i):
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                if pix.n < 5:  # this is GRAY or RGB
                    # pix.writePNG("./data/temp/p%s-%s.png" % (i, xref))
                    pix.writePNG("./data/temp/back_temp.png")
                else:  # CMYK: convert to RGB first
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)
                    # pix1.writePNG("./data/temp/p%s-%s.png" % (i, xref))
                    pix.writePNG("./data/temp/back_temp.png")
                    pix1 = None
                pix = None
        st.image("./data/temp/back_temp.png", use_column_width=True)

    elif extension2 == "png":
        back_image = Image.open(uploaded_file2)

        st.image(back_image, caption='Uploaded Front Image', use_column_width=True)

    elif extension2 == "jpg":

        # SHOW IMAGE IF JPG FORMAT

        back_image = Image.open(uploaded_file1)

        st.image(back_image, caption='Uploaded Front Image', use_column_width=True)


    else:
        st.write("Please upload .JPG, .PNG OR .PDF format file only!")

if st.button('Process Images'):

    if extension2 == "pdf":

        st.write("Processing...")

        startTime = time.time()


        # this functions take the front image of the ID card and returns a string of all the text information in the image
        def textExtractorfront_png():

            # front.jpg is the front of the ID card
            img = cv2.imread('./data/temp/front_temp.png')

            # img = cv2.resize(img, None, fx=2, fy=2)

            # gray = cv2.cvtColor(front_image, cv2.COLOR_BGR2GRAY)

            string = (pytesseract.image_to_string(img))

            store_array = string.split()

            return store_array


        # As most of the functions use this we can calculate this once and reuse to reduce computations
        store_array_front = textExtractorfront_png()


        # print(store_array_front)

        # this functions take the back image of the ID card and returns a string of all the text information in the image
        def textExtractorback_png():

            # back.jpg is the back side of the ID Card
            img = cv2.imread('./data/temp/back_temp.png')

            # img = cv2.resize(img, None, fx=2, fy=2)

            # gray = cv2.cvtColor(back_image, cv2.COLOR_BGR2GRAY)

            string = (pytesseract.image_to_string(img))

            store_array_back = string.split()

            return store_array_back


        # As most of the functions use this we can calculate this once and reuse to reduce computations
        store_array_back = textExtractorback_png()


        # print(store_array_back)

        # this functions uses a regex to find the FIN  in the string returned from the textExtractorfront_jpg function and returns the FIN
        def FIN_ExtractorFromString():

            FIN = ""

            # we do an element wise search to find which element in the array matches with regex of a FIN, this regex will work for both local and foreigner FIN

            for element in store_array_front:

                m = re.match("^[STFG]\d{7}[A-Z]$", element)

                # See if success.
                if m:
                    # print(element)
                    FIN = element

                else:
                    pass
                    # print("No FIN found!")

            for element in store_array_back:

                m = re.match("^[STFG]\d{7}[A-Z]$", element)

                # See if success.
                if m:
                    # print(element)
                    FIN = element

                else:
                    pass
                    # print("No FIN found!")

            return FIN


        # this functions works on the principal that the name of the pass holder lies between the element named 'Name' and element named 'Date'
        # if you print the store_array below you will get ('Name', 'KUMAR', 'SIDDHARTH', 'Date') inside it. We find the index of the element 'Name' and the element
        # "Date" and find all the values from the array with indexes between these two values.

        # this functions returns the Name of the pass holder as a the string
        def Name_ExtractorFromString():

            # we initialize this in case there is no name found by the algorithm we can pass None to know that the algorithm did not find a name
            name = ""

            # finding the index values when the name starts and ends,as the name can be of more than 2 words
            nameStartPosition = int(store_array_front.index('Name')) + 1
            nameEndPosition = int(store_array_front.index('Date')) - 1

            # extracting all the elements with the indexes between the element 'Name' and 'Date'
            nameArray = (store_array_front[nameStartPosition:nameEndPosition + 1])

            # initializing an empty string which will be over written to concatenate the index values from the store_array to make the full name
            nameString = " "

            name = (str(nameString.join(nameArray)))

            # print(name)

            return name


        # this functions uses a regex to find the DOB in the string returned from the textExtractorfront_jpg function and returns the DOB
        def DOB_ExtractorFromString():

            DOB = ""

            # we do an element wise search to find which element in the array matches with regex of a DOB, it should be in the dd-mm-yyyy format
            for element in store_array_front:

                m = re.match("^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$", element)

                # See if success.
                if m:
                    # print(element)
                    DOB = element

                else:
                    # print("No DOB found!")
                    pass

            return DOB


        # this functions uses a regex to find the Expiry date in the string returned from the textExtractorback_jpg function and returns the Expiry
        def Expiry_ExtractorFromString():

            expiry = ""

            # print(store_array)

            # we do an element wise search to find which element in the array matches with regex of a DOB, it should be in the dd-mm-yyyy format
            for element in store_array_back:

                m = re.match("^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$", element)

                # See if success.

                # this automatically selects the later date which is the expiry date
                # there are two dates on the back of the ID card, the first one is date of issue, as the algorithm runs left to right, it overwrites the date of issue
                if m:
                    # print(element)
                    expiry = element

                else:
                    # print("No DOB found!")
                    pass

            return expiry


        FIN = FIN_ExtractorFromString()

        Name = Name_ExtractorFromString()

        DOB = DOB_ExtractorFromString()

        Expiry = Expiry_ExtractorFromString()

        st.write("FIN:", FIN)
        st.write("Name:", Name)
        st.write("Date of birth:", DOB)
        st.write("Pass expires on:", Expiry)

        st.write("It took {0} seconds to process this".format(time.time() - startTime))


        def filedownload(df):
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
            href = f'<a href="data:file/csv;base64,{b64}" download="credentials.csv">Download CSV File</a>'
            return href


        values = {'FIN': [FIN],
                  'Name': [Name],
                  'DOB': [DOB],
                  'Expiry': [Expiry]
                  }

        df = pd.DataFrame(values, columns=['FIN', 'Name', 'DOB', 'Expiry'])

        df.to_csv('./values.csv', index=False, header=True)

        st.markdown(filedownload(df), unsafe_allow_html=True)

    if extension1 == "jpg":
        # THE THE PROCESS IMAGES BUTTON IS PRESSED THEN ONLY CONTINUE WITH THE PROCESSING

        st.write("Processing...")

        # INITIALIZING THE TIME
        startTime = time.time()


        # this functions take the front image of the ID card and returns a string of all the text information in the image
        def textExtractorfront_jpg():

            # front.jpg is the front of the ID card
            # img = cv2.imread('./data/front.jpg')

            # img = cv2.resize(img, None, fx=2, fy=2)

            # gray = cv2.cvtColor(front_image, cv2.COLOR_BGR2GRAY)

            string = (pytesseract.image_to_string(front_image))

            store_array = string.split()

            return store_array


        # As most of the functions use this we can calculate this once and reuse to reduce computations
        store_array_front = textExtractorfront_jpg()


        # print(store_array_front)

        # this functions take the back image of the ID card and returns a string of all the text information in the image
        def textExtractorback_jpg():

            # back.jpg is the back side of the ID Card
            # img = cv2.imread('./data/back.jpg')

            # img = cv2.resize(img, None, fx=2, fy=2)

            # gray = cv2.cvtColor(back_image, cv2.COLOR_BGR2GRAY)

            string = (pytesseract.image_to_string(back_image))

            store_array_back = string.split()

            return store_array_back


        # As most of the functions use this we can calculate this once and reuse to reduce computations
        store_array_back = textExtractorback_jpg()


        # print(store_array_back)

        # this functions uses a regex to find the FIN  in the string returned from the textExtractorfront_jpg function and returns the FIN
        def FIN_ExtractorFromString():

            FIN = ""

            # we do an element wise search to find which element in the array matches with regex of a FIN, this regex will work for both local and foreigner FIN
            for element in store_array_front:

                m = re.match("^[STFG]\d{7}[A-Z]$", element)

                # See if success.
                if m:
                    # print(element)
                    FIN = element

                else:
                    pass
                    # print("No FIN found!")

            return FIN

            for element in store_array_back:

                m = re.match("^[STFG]\d{7}[A-Z]$", element)

                # See if success.
                if m:
                    # print(element)
                    FIN = element

                else:
                    pass
                    # print("No FIN found!")

            return FIN


        # this functions works on the principal that the name of the pass holder lies between the element named 'Name' and element named 'Date'
        # if you print the store_array below you will get ('Name', 'KUMAR', 'SIDDHARTH', 'Date') inside it. We find the index of the element 'Name' and the element
        # "Date" and find all the values from the array with indexes between these two values.

        # this functions returns the Name of the pass holder as a the string
        def Name_ExtractorFromString():

            # we initialize this in case there is no name found by the algorithm we can pass None to know that the algorithm did not find a name
            name = None

            # finding the index values when the name starts and ends,as the name can be of more than 2 words
            nameStartPosition = int(store_array_front.index('Name')) + 1
            nameEndPosition = int(store_array_front.index('Date')) - 1

            # extracting all the elements with the indexes between the element 'Name' and 'Date'
            nameArray = (store_array_front[nameStartPosition:nameEndPosition + 1])

            # initializing an empty string which will be over written to concatenate the index values from the store_array to make the full name
            nameString = " "

            name = (str(nameString.join(nameArray)))

            # print(name)

            return name


        # this functions uses a regex to find the DOB in the string returned from the textExtractorfront_jpg function and returns the DOB
        def DOB_ExtractorFromString():

            # we do an element wise search to find which element in the array matches with regex of a DOB, it should be in the dd-mm-yyyy format
            for element in store_array_front:

                m = re.match("^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$", element)

                # See if success.
                if m:
                    # print(element)
                    DOB = element

                else:
                    # print("No DOB found!")
                    pass

            return DOB


        # this functions uses a regex to find the Expiry date in the string returned from the textExtractorback_jpg function and returns the Expiry
        def Expiry_ExtractorFromString():

            # print(store_array)

            # we do an element wise search to find which element in the array matches with regex of a DOB, it should be in the dd-mm-yyyy format
            for element in store_array_back:

                m = re.match("^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$", element)

                # See if success.

                # this automatically selects the later date which is the expiry date
                # there are two dates on the back of the ID card, the first one is date of issue, as the algorithm runs left to right, it overwrites the date of issue
                if m:
                    # print(element)
                    expiry = element

                else:
                    # print("No DOB found!")
                    pass

            return expiry


        FIN = FIN_ExtractorFromString()

        Name = Name_ExtractorFromString()

        DOB = DOB_ExtractorFromString()

        Expiry = Expiry_ExtractorFromString()

        st.write("FIN:", FIN)
        st.write("Name:", Name)
        st.write("Date of birth:", DOB)
        st.write("Pass expires on:", Expiry)

        st.write("It took {0} seconds to process this".format(time.time() - startTime))


        # THIS FUNCTION PROVIDES THE DOWNLOAD CAPABILITY
        def filedownload(df):
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
            href = f'<a href="data:file/csv;base64,{b64}" download="credentials.csv">Download CSV File</a>'
            return href


        values = {'FIN': [FIN],
                  'Name': [Name],
                  'DOB': [DOB],
                  'Expiry': [Expiry]
                  }

        df = pd.DataFrame(values, columns=['FIN', 'Name', 'DOB', 'Expiry'])

        df.to_csv('./values.csv', index=False, header=True)

        st.markdown(filedownload(df), unsafe_allow_html=True)

    if extension1 == "png":
        st.write("Processing...")

        startTime = time.time()


        # this functions take the front image of the ID card and returns a string of all the text information in the image
        def textExtractorfront_png():

            # front.jpg is the front of the ID card
            # img = cv2.imread('./data/front.jpg')

            # img = cv2.resize(img, None, fx=2, fy=2)

            # gray = cv2.cvtColor(front_image, cv2.COLOR_BGR2GRAY)

            string = (pytesseract.image_to_string(front_image))

            store_array = string.split()

            return store_array


        # As most of the functions use this we can calculate this once and reuse to reduce computations
        store_array_front = textExtractorfront_png()


        # print(store_array_front)

        # this functions take the back image of the ID card and returns a string of all the text information in the image
        def textExtractorback_png():

            # back.jpg is the back side of the ID Card
            # img = cv2.imread('./data/back.jpg')

            # img = cv2.resize(img, None, fx=2, fy=2)

            # gray = cv2.cvtColor(back_image, cv2.COLOR_BGR2GRAY)

            string = (pytesseract.image_to_string(back_image))

            store_array_back = string.split()

            return store_array_back


        # As most of the functions use this we can calculate this once and reuse to reduce computations
        store_array_back = textExtractorback_png()


        # print(store_array_back)

        # this functions uses a regex to find the FIN  in the string returned from the textExtractorfront_jpg function and returns the FIN
        def FIN_ExtractorFromString():

            FIN = ""

            # we do an element wise search to find which element in the array matches with regex of a FIN, this regex will work for both local and foreigner FIN

            for element in store_array_front:

                m = re.match("^[STFG]\d{7}[A-Z]$", element)

                # See if success.
                if m:
                    # print(element)
                    FIN = element

                else:
                    pass
                    # print("No FIN found!")

            for element in store_array_back:

                m = re.match("^[STFG]\d{7}[A-Z]$", element)

                # See if success.
                if m:
                    # print(element)
                    FIN = element

                else:
                    pass
                    # print("No FIN found!")

            return FIN


        # this functions works on the principal that the name of the pass holder lies between the element named 'Name' and element named 'Date'
        # if you print the store_array below you will get ('Name', 'KUMAR', 'SIDDHARTH', 'Date') inside it. We find the index of the element 'Name' and the element
        # "Date" and find all the values from the array with indexes between these two values.

        # this functions returns the Name of the pass holder as a the string
        def Name_ExtractorFromString():

            # we initialize this in case there is no name found by the algorithm we can pass None to know that the algorithm did not find a name
            name = None

            # finding the index values when the name starts and ends,as the name can be of more than 2 words
            nameStartPosition = int(store_array_front.index('Name')) + 1
            nameEndPosition = int(store_array_front.index('Date')) - 1

            # extracting all the elements with the indexes between the element 'Name' and 'Date'
            nameArray = (store_array_front[nameStartPosition:nameEndPosition + 1])

            # initializing an empty string which will be over written to concatenate the index values from the store_array to make the full name
            nameString = " "

            name = (str(nameString.join(nameArray)))

            # print(name)

            return name


        # this functions uses a regex to find the DOB in the string returned from the textExtractorfront_jpg function and returns the DOB
        def DOB_ExtractorFromString():

            # we do an element wise search to find which element in the array matches with regex of a DOB, it should be in the dd-mm-yyyy format
            for element in store_array_front:

                m = re.match("^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$", element)

                # See if success.
                if m:
                    # print(element)
                    DOB = element

                else:
                    # print("No DOB found!")
                    pass

            return DOB


        # this functions uses a regex to find the Expiry date in the string returned from the textExtractorback_jpg function and returns the Expiry
        def Expiry_ExtractorFromString():

            # print(store_array)

            # we do an element wise search to find which element in the array matches with regex of a DOB, it should be in the dd-mm-yyyy format
            for element in store_array_back:

                m = re.match("^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$", element)

                # See if success.

                # this automatically selects the later date which is the expiry date
                # there are two dates on the back of the ID card, the first one is date of issue, as the algorithm runs left to right, it overwrites the date of issue
                if m:
                    # print(element)
                    expiry = element

                else:
                    # print("No DOB found!")
                    pass

            return expiry


        FIN = FIN_ExtractorFromString()

        Name = Name_ExtractorFromString()

        DOB = DOB_ExtractorFromString()

        Expiry = Expiry_ExtractorFromString()

        st.write("FIN:", FIN)
        st.write("Name:", Name)
        st.write("Date of birth:", DOB)
        st.write("Pass expires on:", Expiry)

        st.write("It took {0} seconds to process this".format(time.time() - startTime))


        def filedownload(df):
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
            href = f'<a href="data:file/csv;base64,{b64}" download="credentials.csv">Download CSV File</a>'
            return href


        values = {'FIN': [FIN],
                  'Name': [Name],
                  'DOB': [DOB],
                  'Expiry': [Expiry]
                  }

        df = pd.DataFrame(values, columns=['FIN', 'Name', 'DOB', 'Expiry'])

        df.to_csv('./values.csv', index=False, header=True)

        st.markdown(filedownload(df), unsafe_allow_html=True)

