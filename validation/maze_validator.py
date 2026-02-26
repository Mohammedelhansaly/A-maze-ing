from pydantic import BaseModel, Field, model_validator, field_validator


class mazeValidator(BaseModel):
    width: int = Field(..., gt=5, lt=100)
    height: int = Field(..., gt=5, lt=100)
    entry: tuple[int, int]
    exit_: tuple[int, int]

    @field_validator("entry", "exit_")
    @classmethod
    def validate_cordinate(cls, v):
        x, y = v
        if x < 0 and y < 0:
            raise ValueError("cordinates must be non-negative")
        return v

    @model_validator(mode="after")
    def validate_entry_exit(self):
        if not (0 <= self.entry[0] < self.width and
                0 <= self.entry[1] < self.height):
            raise ValueError("Entry point is out of maze bounds")
        if not (0 <= self.exit_[0] < self.width and
                0 <= self.exit_[1] < self.height):
            raise ValueError("Exit point is out of maze bounds")
        if self.entry == self.exit_:
            raise ValueError("Entry and exit points cannot be the same")
        return self
