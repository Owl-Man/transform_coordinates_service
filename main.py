from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
from transform_coordinates import transform_coordinates, load_parameters
from generate_report import generate_markdown_report

app = FastAPI(title="Coordinate Transformation Service")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/coordinate-systems")
async def get_coordinate_systems():
    return {"systems": list(load_parameters().keys())}

@app.post("/transform")
async def transform_file(
    file: UploadFile = File(...),
    source_system: str = Form(...)
):
    try:
        # Read the Excel file
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))
        
        # Validate input data
        required_columns = ['Name', 'X', 'Y', 'Z']
        if not all(col in df.columns for col in required_columns):
            raise HTTPException(
                status_code=400,
                detail=f"Input file must contain columns: {', '.join(required_columns)}"
            )
        
        # Transform coordinates
        transformed_df, formulas, params = transform_coordinates(df, source_system)
        
        # Generate markdown report
        report = generate_markdown_report(df, transformed_df, formulas, params)
        
        return {"report": report}
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 