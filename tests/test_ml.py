import pytest
import numpy as np

try:
    from resume_scanner.ml.embeddings import SemanticEncoder, SECTION_ALIGNMENT
    from resume_scanner.ml.features import FeatureExtractor, FEATURE_SCHEMA
    from resume_scanner.ml.dataset import ResumeJDDatasetGenerator, DatasetValidator
    from resume_scanner.ml.model import ModelTrainer
    from resume_scanner.ml.inference import HybridMatcher
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False


@pytest.mark.skipif(not ML_AVAILABLE, reason="ML dependencies not installed")
class TestMLEngine:
    
    def test_semantic_encoder_initialization(self):
        encoder = SemanticEncoder("all-MiniLM-L6-v2")
        assert encoder.embedding_dim == 384
        
        text = "Machine learning engineer"
        vec = encoder.encode_text(text)
        assert vec.shape == (384,)
        
    def test_semantic_similarity_sanity(self):
        encoder = SemanticEncoder("all-MiniLM-L6-v2")
        
        sim1 = encoder.similarity("Python developer", "Software engineer writing Python")
        sim2 = encoder.similarity("Python developer", "Registered Nurse")
        
        assert sim1 > sim2
        
    def test_feature_extractor_schema(self):
        extractor = FeatureExtractor(encoder=None)
        features = extractor.extract("Resume text", "JD text")
        
        assert len(features) == len(FEATURE_SCHEMA)
        for key in FEATURE_SCHEMA:
            assert key in features
            assert isinstance(features[key], float)
            
    def test_dataset_generator(self):
        gen = ResumeJDDatasetGenerator(seed=42)
        entries = gen.generate(pairs_per_domain=2)
        
        assert len(entries) > 0
        
        validator = DatasetValidator()
        report = validator.validate(entries)
        
        assert report["is_valid"] is True
        assert report["positive_pairs"] > 0
        assert report["negative_pairs"] > 0
        
    def test_model_trainer_pipeline(self):
        # Generate tiny dataset
        gen = ResumeJDDatasetGenerator(seed=42)
        entries = gen.generate(pairs_per_domain=5)
        
        extractor = FeatureExtractor(encoder=None)
        
        X = []
        y = []
        for e in entries:
            X.append(extractor.extract_vector(e.resume_text, e.job_description))
            y.append(e.match_label)
            
        X = np.array(X)
        y = np.array(y)
        
        # Test just that it doesn't crash
        trainer = ModelTrainer(feature_names=FEATURE_SCHEMA)
        results = trainer.train_and_compare(X, y, X, y, n_cv_folds=2)
        
        assert "comparison" in results
        assert results["best_model"] is not None
        
    def test_hybrid_matcher_graceful_degradation(self):
        matcher = HybridMatcher(encoder=None, model=None)
        assert not matcher.has_encoder
        assert not matcher.has_model
        
        result = matcher.match("Resume", "JD", {}, {}, {})
        assert result is None
