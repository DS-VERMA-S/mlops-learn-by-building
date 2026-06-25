# Block 4 — Model Registry + Promotion (1 hr)

**Concept:** MLflow Model Registry has stages => None → Staging → Production. In a real pipeline, you promote a model only after it passes evaluation. You must understand this transition.


**Question**

- What is the difference between a run and a registered model in MLflow?
    - A run is a recorded experiment execution — it captures params, metrics, and artifacts for one training attempt. It lives on your MLflow server already. A registered model is a named, versioned entity that points to a specific run's artifacts and has a lifecycle (Staging/Production). The key difference: runs are ephemeral experiment records, registered models are deployable versioned artifacts with promotion workflows.

- Right now your serving layer will load the model using models:/IrisClassifier/Production. What happens if you register version 2 and promote it to Production — does the serving layer automatically pick it up or not?
    - Your serving layer loads models:/IrisClassifier/Production at startup. Whatever model is tagged Production at that moment gets loaded. If you promote version 2 to Production later, the serving layer will NOT switch — it already loaded version 1 at startup and holds it in memory. To pick up version 2 you need to restart the serving container. That's a critical production consideration — model updates require a deployment step, not just a registry promotion.

python '.\day1\Block 4 - Model Registry\registry.py'
