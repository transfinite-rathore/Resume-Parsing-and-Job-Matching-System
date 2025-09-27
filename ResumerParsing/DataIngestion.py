import fitz

def read_pdf(path:str) -> str:
    try:
        if(len(path)==0):
            return "Path is empty"
        elif(path.split(".")[-1]!="pdf"):
            return "File Format is not PDF"
        else:
            
            pdf_file=fitz.open(path)
            docs=""
            for page in range(len(pdf_file)):
                data=pdf_file[page].get_text()
                docs+=data
    except Exception as e:
        raise e
    return docs