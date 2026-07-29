import joblib

model = joblib.load("mortgage_model.pkl")

print("Model type:")
print(type(model))

if hasattr(model, "named_steps"):
    print("\n✅ This is a Pipeline")
    print("\nPipeline steps:")
    print(model.named_steps)
else:
    print("\n❌ This is NOT a Pipeline")