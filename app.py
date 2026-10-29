"""App B: procesa mediciones en memoria; no las comunica a la plataforma."""
from fastapi import FastAPI
from qos_faults import FaultProfile
fault_profile = FaultProfile()
app=FastAPI()
events=0
@app.get('/health')
def health():return {'status':'ok'}
@app.get('/metrics')
def metrics():return fault_profile.decorate({'response_time_ms':25,'execution_time':4,'availability':24,'reliability':0.02,'cost':0.11,'status':'ok'})
@app.post('/save')
def save(payload:dict):
    global events
    events+=1
    return {'ok':True}

@app.get('/internal-count')
def internal_count(): return {'processed':events}


@app.post('/admin/simulate')
def inject_qos_fault(payload: dict):
    """Modifica TEMPORALMENTE métricas expuestas por este contenedor real."""
    from fastapi import HTTPException
    try:
        return fault_profile.inject(payload)
    except (ValueError, TypeError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
