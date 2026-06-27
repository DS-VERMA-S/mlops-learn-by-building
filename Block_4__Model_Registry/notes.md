# Block 4 — Model Registry + Promotion

## Summary

This block demonstrates registering models in MLflow's Model Registry and promoting them through stages (None → Staging → Production). The registry provides a canonical, versioned place to track deployable models.

## Quick Checklist

- [x] Register a trained model from a run
- [x] Create/stage versions and promote to `Staging` and `Production`
- [x] Observe how promotion affects serving

## Key Concepts (plain English)

- Run vs Registered Model: A run is an experiment record (params, metrics, artifacts). A registered model is a named, versioned pointer to a run's artifacts with a lifecycle and metadata.
- Promotion does not automatically change running services: most serving processes load a model at startup. Promoting to Production changes the registry state; your service must reload or be redeployed to pick up the new version.

## Example

```bash
python day1/Block\ 4\ -\ Model\ Registry/registry.py
```

## Verification

- Check the MLflow UI under "Models" for versions and stages.
- Confirm serving behavior by promoting a new version and restarting the serving process to load it.

## Issues Faced

- Registered models did not appear because the model was not created or registered correctly.
- Promotion to a new stage did not impact running services until the serving process reloaded the model.
- Stage transitions could be blocked by insufficient registry permissions or incorrect access settings.

## Key Learnings

- The Model Registry provides a versioned lifecycle for models separate from experiment runs.
- Promoting a model is a metadata change; serving applications must refresh or redeploy to use it.
- Use both the MLflow UI and registry APIs to manage model versions and stages safely.

