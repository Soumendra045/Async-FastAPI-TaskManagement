from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# print(pwd_context.hash("silu@0045"))
print(
    pwd_context.verify(
        "silu@0045",
        "$2b$12$vMD1PVdlwDXl6QRYjJKwr.NzfXdpmnIPN9A.wjFkj/j7T5XLCw.eu"
    )
)
