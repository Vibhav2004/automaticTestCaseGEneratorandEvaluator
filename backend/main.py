from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import analyzer, generator, executor, api_tester, samples, web_tester

app = FastAPI(
    title="AutoTestAI API",
    description="Intelligent Dynamic Test Case Generator & Executor",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "https://mjproject-f13dgjyyc-vibhav2004s-projects.vercel.app"
],
allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(analyzer.router, prefix="/api/v1", tags=["Analyzer"])
app.include_router(generator.router, prefix="/api/v1", tags=["Generator"])
app.include_router(executor.router, prefix="/api/v1", tags=["Executor"])
app.include_router(api_tester.router, prefix="/api/v1", tags=["API Tester"])
app.include_router(samples.router, prefix="/api/v1/samples", tags=["Samples"])
app.include_router(web_tester.router, prefix="/api/v1", tags=["Web Tester"])

@app.get("/")
async def root():
    return {"message": "Welcome to AutoTestAI API", "status": "running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
