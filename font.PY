import sys
import fitz

def extract_text_from_area(pdf_path, page_number, x_min, x_max, y_min, y_max):
    try:
        doc = fitz.open(pdf_path)
        page = doc[page_number]

        blocks = page.get_text("dict", flags=11)["blocks"]
        extracted_text = ""

        for b in blocks:
            for l in b["lines"]:
                for s in l["spans"]:
                    if (
                        x_min <= s["bbox"][0] <= x_max and
                        y_min <= s["bbox"][1] <= y_max
                    ):
                        extracted_text += s["text"]
        
        doc.close()
        return extracted_text.strip()
    except Exception as e:
        print("Error occurred while extracting text:", str(e))
        return ""

pdf_path = "15Feb.pdf"  # Specify the path to your PDF file here
page_number = 3
x_min = 298  # Minimum x-coordinate of the selected area
x_max = 545  # Maximum x-coordinate of the selected area
y_min = 580  # Minimum y-coordinate of the selected area
y_max = 772  # Maximum y-coordinate of the selected area

extracted_text = extract_text_from_area(pdf_path, page_number, x_min, x_max, y_min, y_max)
print(extracted_text)

# import sys
# import fitz

# def flags_decomposer(flags):
#     """Make font flags human readable."""
#     l = []
#     if flags & 2 ** 0:
#         l.append("superscript")
#     # if flags & 2 ** 1:
#     #     l.append("italic")
#     # if flags & 2 ** 2:
#     #     l.append("serifed")
#     # else:
#     #     l.append("sans")
#     # if flags & 2 ** 3:
#     #     l.append("monospaced")
#     # else:
#     #     l.append("proportional")
#     # if flags & 2 ** 4:
#     #     l.append("bold")
#     return ", ".join(l)

# pdf_path = "shorya_times_27_ May-2023.pdf"  # Specify the path to your PDF file here

# doc = fitz.open(pdf_path)
# page = doc[1]

# blocks = page.get_text("dict", flags=11)["blocks"]
# # print(blocks)
# sorted_blocks = sorted(blocks, key=lambda b: (b["bbox"][0], b["bbox"][1]))
# for b in sorted_blocks:  # Iterate through the text blocks
#     # print("hello",type(b),b)
#     block_text = ""
#     # print("heeloo",type(sorted_blocks))
#     for l in b["lines"]:  # Iterate through the text lines
#         for s in l["spans"]:  # Iterate through the text spans
#             block_text += s["text"]  # Concatenate the text within the block
#     print("")
#     font_properties = "Font: '%s' (%s), size %g, color #%06x" % (
#         b["lines"][0]["spans"][0]["font"],  # Font name of the first span in the first line
#         flags_decomposer(b["lines"][0]["spans"][
#             0]["flags"]),  # Readable font flags of the first span in the first line
#         b["lines"][0]["spans"][0]["size"],  # Font size of the first span in the first line
#         b["lines"][0]["spans"][0]["color"],  # Font color of the first span in the first line
#     )
    
#     print(font_properties,block_text)  # Print the merged text within the block
    # print(block_text)
    # print(font_properties)


# import sys
# import fitz

# pdf_path = "15Feb.pdf"  # Specify the path to your PDF file here

# doc = fitz.open(pdf_path)
# page = doc[1]

# # Read page text as a list of dictionaries
# blocks = page.get_text("dict", flags=11)["blocks"]

# # Initialize an empty dictionary to store the key-value pairs
# text_dict = {}
# sorted_blocks = sorted(blocks, key=lambda b: (b["bbox"][0], b["bbox"][1]))
# for b in sorted_blocks:  # Iterate through the text blocks
#     block_text = ""
#     font_size = b["lines"][0]["spans"][0]["size"]  # Font size of the first span in the first line
#     for l in b["lines"]:  # Iterate through the lines in the block
#         for s in l["spans"]:  # Iterate through the spans in the line
#             block_text += s["text"]  # Concatenate the text within the block

#     if 22 <= font_size <= 50:  # Check if font size is between 22 and 50
#         key = block_text.strip()
#         if key not in text_dict:
#             text_dict[key] = None
#     elif font_size < 20:  # Check if font size is between 10 and 15
#         value = block_text.strip()
#         print("Value:", value)
#         if len(text_dict) > 0:
#             last_key = list(text_dict.keys())[-1]
#             text_dict[last_key] = value

# print("Key-Value Pairs:")
# for key, value in text_dict.items():
#     print("Key:", key)
#     print("Value:", value)
#     print()

# import sys
# import fitz

# pdf_path = "15Feb.pdf"  # Specify the path to your PDF file here

# doc = fitz.open(pdf_path)
# page = doc[1]

# # Read page text as a list of dictionaries
# blocks = page.get_text("dict", flags=11)["blocks"]

# # Sort blocks by top-to-bottom and left-to-right coordinates
# sorted_blocks = sorted(blocks, key=lambda b: (b["bbox"][1], b["bbox"][0]))

# # Initialize an empty dictionary to store the key-value pairs
# text_dict = {}
# prev_y = None  # Track the previous block's y-coordinate

# for b in sorted_blocks:  # Iterate through the text blocks
#     block_text = ""
#     font_size = b["lines"][0]["spans"][0]["size"]  # Font size of the first span in the first line

#     for l in b["lines"]:  # Iterate through the lines in the block
#         for s in l["spans"]:  # Iterate through the spans in the line
#             block_text += s["text"]  # Concatenate the text within the block

#     if prev_y is None or b["bbox"][1] > prev_y:  # Check if block is on a new line
#         if len(text_dict) > 0:
#             last_key = list(text_dict.keys())[-1]
#             text_dict[last_key] = block_text.strip()  # Update the value for the last key

#     if 22 <= font_size <= 50:  # Check if font size is between 22 and 50
#         key = block_text.strip()
#         text_dict[key] = None  # Add key to the dictionary

#     prev_y = b["bbox"][1]  # Update the previous y-coordinate

# # Set the value for the last key
# if len(text_dict) > 0:
#     last_key = list(text_dict.keys())[-1]
#     text_dict[last_key] = block_text.strip()

# print("Key-Value Pairs:")
# for key, value in text_dict.items():
#     print("Key:", key)
#     print("Value:", value)
#     print()


# import sys
# import fitz

# pdf_path = "shorya_times_27_ May-2023.pdf"  # Specify the path to your PDF file here

# doc = fitz.open(pdf_path)
# page = doc[1]

# # Read page text as a list of dictionaries
# blocks = page.get_text("dict", flags=11)["blocks"]

# # Sort blocks by top-to-bottom and left-to-right coordinates
# sorted_blocks = sorted(blocks, key=lambda b: (b["bbox"][3], b["bbox"][0]))

# # Initialize an empty dictionary to store the key-value pairs
# text_dict = {}
# current_key = None  # Track the current key

# # Define the direction of iteration
# direction = "top_to_bottom_left_to_right"

# if direction == "top_to_bottom_left_to_right":
#     for b in sorted_blocks:  # Iterate through the text blocks
#         block_text = ""
#         font_size = b["lines"][0]["spans"][0]["size"]  # Font size of the first span in the first line

#         for l in b["lines"]:  # Iterate through the lines in the block
#             for s in l["spans"]:  # Iterate through the spans in the line
#                 block_text += s["text"]  # Concatenate the text within the block

#         if 22 <= font_size <= 50:  # Check if font size is between 22 and 50
#             current_key = block_text.strip()  # Set the current key
#             text_dict[current_key] = None  # Add key to the dictionary
#         elif 10 <= font_size <= 15:  # Check if font size is between 10 and 15
#             if current_key is not None:
#                 value = block_text.strip()
#                 if text_dict[current_key] is None:
#                     text_dict[current_key] = value
#                 else:
#                     text_dict[current_key] += " " + value

# elif direction == "top_to_bottom_right_to_left":
#     for b in reversed(sorted_blocks):  # Iterate through the text blocks in reverse order
#         block_text = ""
#         font_size = b["lines"][0]["spans"][0]["size"]  # Font size of the first span in the first line

#         for l in b["lines"]:  # Iterate through the lines in the block
#             for s in l["spans"]:  # Iterate through the spans in the line
#                 block_text += s["text"]  # Concatenate the text within the block

#         if 22 <= font_size <= 50:  # Check if font size is between 22 and 50
#             current_key = block_text.strip()  # Set the current key
#             text_dict[current_key] = None  # Add key to the dictionary
#         elif 10 <= font_size <= 15:  # Check if font size is between 10 and 15
#             if current_key is not None:
#                 value = block_text.strip()
#                 if text_dict[current_key] is None:
#                     text_dict[current_key] = value
#                 else:
#                     text_dict[current_key] += " " + value

# else:
#     print("Invalid direction specified.")

# print("Key-Value Pairs:")
# for key, value in text_dict.items():
#     print("Key:", key)
#     print("Value:", value)
#     print()


