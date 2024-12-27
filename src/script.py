import os
import sys
import re
from pathlib import Path
from typing import List, Literal, Tuple
from PyPDF2 import PdfWriter, PdfReader, errors

# Add parent directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

class PDFUtils:
    """
    A utility class for various PDF manipulation operations.
    """
    
    @staticmethod
    def get_bookmarks(bookmark_list: list, reader: PdfReader) -> dict:
        """
        Convert bookmark list to dictionary mapping page numbers to titles.
        
        Args:
            bookmark_list (list): List of bookmarks
            reader (PdfReader): PDF reader object
        
        Returns:
            dict: Dictionary of page numbers to bookmark titles
        """
        result = {}
        if not bookmark_list:
            return result
        
        for item in bookmark_list:
            if isinstance(item, list):
                # Recursively process nested bookmark lists
                nested_bookmarks = PDFUtils.get_bookmarks(item, reader)
                result.update(nested_bookmarks)
            else:
                try:
                    title = item.title
                    page_num = item.page
                    
                    if isinstance(page_num, (int, float)):
                        result[page_num] = title
                except Exception as e:
                    print(f"Warning: Could not process bookmark {item}: {e}")
        
        return result

    @staticmethod
    def merge_pdfs(
        pdf_files: List[Path], 
        source_pdf_path: Path, 
        out_pdf_path: Path, 
        mode: Literal['append', 'write'] = 'write'
    ) -> bool:
        """
        Merge PDF files while preserving existing bookmarks.
        
        Args:
            pdf_files (List[Path]): List of PDF files to merge
            source_pdf_path (Path): Path to the source PDF (for append mode)
            out_pdf_path (Path): Output path for merged PDF
            mode (Literal['append', 'write']): Merge mode
        
        Returns:
            bool: True if merge successful, False otherwise
        """
        try:
            writer = PdfWriter()
            page_num_counter = 0
            
            # Validate input files exist
            if not all(file.exists() for file in pdf_files):
                missing = [str(f) for f in pdf_files if not f.exists()]
                raise FileNotFoundError(f"Missing input files: {', '.join(missing)}")

            # Handle append mode
            if mode == 'append' and source_pdf_path.exists():
                try:
                    reader = PdfReader(source_pdf_path)
                    outlines = PDFUtils.get_bookmarks(reader.outline, reader)
                    
                    # Add existing pages and their bookmarks
                    for page_idx, page in enumerate(reader.pages):
                        writer.add_page(page)
                        if page_idx in outlines:
                            writer.add_outline_item(outlines[page_idx], page_idx)
                        page_num_counter += 1
                        
                except Exception as e:
                    print(f"Error reading {source_pdf_path}: {e}. Switching to write mode.")
                    mode = 'write'
                    writer = PdfWriter()
                    page_num_counter = 0

            # Merge additional files
            for file in pdf_files:
                try:
                    pdf_reader = PdfReader(file)
                    
                    # Handle encrypted PDFs
                    if pdf_reader.is_encrypted:
                        try:
                            pdf_reader.decrypt('')
                        except errors.PdfReadError:
                            print(f"Error decrypting file {file}: Unsupported encryption")
                            continue
                    
                    num_pages = len(pdf_reader.pages)
                    
                    if num_pages == 0:
                        print(f"Warning: {file} has no pages, skipping")
                        continue
                    
                    # Add bookmark for the file
                    filename = file.stem
                    writer.add_outline_item(filename, page_num_counter)
                    
                    # Add pages
                    for page in pdf_reader.pages:
                        writer.add_page(page)
                    page_num_counter += num_pages
                    
                except Exception as e:
                    print(f"Error processing file {file}: {e}")
                    continue

            # Ensure output directory exists
            out_pdf_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write merged PDF to output
            with open(out_pdf_path, 'wb') as pdf_file:
                writer.write(pdf_file)
            
            print(f"Successfully merged PDF to: {out_pdf_path}")
            return True
            
        except Exception as e:
            print(f"Critical error during merge: {e}")
            return False

    @staticmethod
    def split_pdf_range(
        input_file: Path, 
        output_file: Path, 
        start: int, 
        end: int
    ) -> None:
        """
        Split a PDF into a specific page range.
        
        Args:
            input_file (Path): Source PDF file
            output_file (Path): Output PDF file
            start (int): Starting page number (1-indexed)
            end (int): Ending page number (1-indexed)
        """
        reader = PdfReader(input_file)
        writer = PdfWriter()
        
        # Add specified pages to the writer
        for page_num in range(start - 1, end):
            if 0 <= page_num < len(reader.pages):
                writer.add_page(reader.pages[page_num])
            else:
                print(f"Page {page_num} is out of range for this PDF.")
        
        with open(output_file, "wb") as output_file:
            writer.write(output_file)
        print(f"Done splitting: {output_file}")

    @staticmethod
    def split_custom_ranges(
        input_file: Path, 
        output_prefix: str, 
        ranges: List[Tuple[int, int]]
    ) -> None:
        """
        Split a PDF into multiple custom page ranges.
        
        Args:
            input_file (Path): Source PDF file
            output_prefix (str): Prefix for output filenames
            ranges (List[Tuple[int, int]]): List of page ranges to extract
        """
        try:
            dir_path = os.path.dirname(input_file)
            reader = PdfReader(input_file)

            for start, end in ranges:
                if start < 1 or end > len(reader.pages):
                    print(f"Invalid range: {start}-{end}. Skipping.")
                    continue
                
                writer = PdfWriter()
                for page_num in range(start - 1, end):  
                    writer.add_page(reader.pages[page_num])
                
                output_pdf_file = os.path.join(dir_path, f"{output_prefix}-{start}-{end}.pdf")
                with open(output_pdf_file, 'wb') as pdf:
                    writer.write(pdf)
                print(f"Done splitting: {output_pdf_file}")
        
        except Exception as err:
            print(f"Error during splitting process: {err}")

    @staticmethod
    def insert_pages(
        input_pdf: Path, 
        pages_to_insert: Path, 
        position: int, 
        output_pdf: Path
    ) -> None:
        """
        Insert pages from one PDF into another at a specified position.
        
        Args:
            input_pdf (Path): Original PDF file
            pages_to_insert (Path): PDF with pages to insert
            position (int): Page position to insert at (0-indexed)
            output_pdf (Path): Output PDF file
        """
        try:
            # Read the original PDF and pages to insert
            original_reader = PdfReader(input_pdf)
            insert_reader = PdfReader(pages_to_insert)

            # Ensure the file with pages to insert contains pages
            if len(insert_reader.pages) == 0:
                raise ValueError(f"The file {pages_to_insert} contains no pages.")

            writer = PdfWriter()

            # Add pages up to the insertion point
            for i, page in enumerate(original_reader.pages):
                if i == position:  # Insert here
                    for insert_page in insert_reader.pages:
                        writer.add_page(insert_page)
                writer.add_page(page)

            # If position is beyond the last page, append the insert pages at the end
            if position >= len(original_reader.pages):
                for insert_page in insert_reader.pages:
                    writer.add_page(insert_page)

            # Write the resulting PDF to the output file
            with open(output_pdf, 'wb') as output_file:
                writer.write(output_file)

            print(f"Pages inserted successfully. Output saved to {output_pdf}")
        
        except Exception as e:
            print(f"An error occurred: {e}")

    @staticmethod
    def cut_pages(
        ranges: List[Tuple[int, int]], 
        pdf_source_path: Path, 
        output_pdf_path: Path
    ) -> bool:
        """
        Remove pages within specified ranges from a PDF.
        
        Args:
            ranges (List[Tuple[int, int]]): Page ranges to remove (1-indexed)
            pdf_source_path (Path): Source PDF file
            output_pdf_path (Path): Output PDF file
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            reader = PdfReader(pdf_source_path)
            writer = PdfWriter()

            # Precompute the pages to remove
            pages_to_remove = set(
                page_num
                for start, end in ranges
                for page_num in range(start - 1, end)
            )

            # Add only the pages not in the removal set
            for index, page in enumerate(reader.pages):
                if index not in pages_to_remove:
                    writer.add_page(page)

            # Write the result to the output file
            with output_pdf_path.open("wb") as pdf_file:
                writer.write(pdf_file)

            print(f"Successfully cut pages. Saved new file to: {output_pdf_path}.")
            return True
        
        except Exception as e:
            print(f"Error during page cutting: {e}")
            return False

    @staticmethod
    def insert_bookmarks(
        bookmark_names: List[str], 
        bookmark_page_nums: List[int], 
        pdf_source_file: Path, 
        out_pdf_file: Path
    ) -> bool:
        """
        Insert bookmarks into a PDF file.
        
        Args:
            bookmark_names (List[str]): List of bookmark titles
            bookmark_page_nums (List[int]): Corresponding page numbers
            pdf_source_file (Path): Source PDF file
            out_pdf_file (Path): Output PDF file
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Validate input lists
            if len(bookmark_names) != len(bookmark_page_nums):
                print("Error: Bookmark names and page numbers lists must have the same length.")
                return False

            reader = PdfReader(pdf_source_file)
            writer = PdfWriter()
            
            bookmark_data = {
                num_page - 1: name for name, num_page in zip(bookmark_names, bookmark_page_nums)
            }
            
            for page_num, page in enumerate(reader.pages):
                if page_num in bookmark_data:
                    writer.add_outline_item(bookmark_data[page_num], page_num)
                writer.add_page(page)
            
            with open(out_pdf_file, 'wb') as pdf_file:
                writer.write(pdf_file)
            
            print(f"Successfully added bookmarks. Saved new file to: {out_pdf_file}.")
            return True
        
        except Exception as e:
            print(f"Critical error during bookmark insertion: {e}")
            return False

def main():
    pass

if __name__ == "__main__":
    main()