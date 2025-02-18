import os
from functools import reduce

model_name = context.current_model.name if context.current_model else "GLOBAL"

output = f"Model name: {model_name}"

temp_dir = os.environ["temp_dir"]
print(temp_dir)
write_dir = open(reduce(os.path.join, [temp_dir, model_name + ".after.txt"]), "w")
write_dir.write(output)
write_dir.close()
