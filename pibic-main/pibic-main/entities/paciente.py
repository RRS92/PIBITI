from pydantic import BaseModel, validator

age_max = 140
age_min = 0

class Paciente(BaseModel):
    nome: str
    cpf: str
    pre_hematocrit: float
    pre_hemoglobin: float
    pre_lactate: float
    height: float
    redo: int  # 0 ou 1 (booleano)
    cpb: float
    anoxia: float
    female: int  # 0 ou 1 (booleano)
    normothermia: int  # 0 ou 1 (booleano)
    age: int = None  # Incluído conforme tabela (opcional no código)
    hb: float = None # Incluído conforme tabela (opcional no código)
    probability: str = None
    prediction: str = None
    imagem: str = None

    def __repr__(self):
        return f'<Paciente {self.nome}>'

    @validator('redo', 'female', 'normothermia')
    def validate_binary(cls, v):
        if v not in [0, 1]:
            raise ValueError(f'Valor inválido para campo binário: {v}')
        return v

    @validator('age')
    def validate_age(cls, v):
        if v is not None and not (age_min <= v <= age_max):
            raise ValueError('A idade deve estar entre 0 e 140')
        return v
