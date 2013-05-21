import org.apache.mahout.cf.taste.common.TasteException;
import org.apache.mahout.cf.taste.eval.IRStatistics;
import org.apache.mahout.cf.taste.eval.RecommenderBuilder;
import org.apache.mahout.cf.taste.eval.RecommenderEvaluator;
import org.apache.mahout.cf.taste.eval.RecommenderIRStatsEvaluator;
import org.apache.mahout.cf.taste.impl.eval.AverageAbsoluteDifferenceRecommenderEvaluator;
import org.apache.mahout.cf.taste.impl.eval.GenericRecommenderIRStatsEvaluator;
import org.apache.mahout.cf.taste.impl.eval.RMSRecommenderEvaluator;
import org.apache.mahout.cf.taste.impl.model.file.FileDataModel;
import org.apache.mahout.cf.taste.impl.recommender.GenericItemBasedRecommender;
import org.apache.mahout.cf.taste.impl.similarity.EuclideanDistanceSimilarity;
import org.apache.mahout.cf.taste.impl.similarity.LogLikelihoodSimilarity;
import org.apache.mahout.cf.taste.impl.similarity.PearsonCorrelationSimilarity;
import org.apache.mahout.cf.taste.impl.similarity.TanimotoCoefficientSimilarity;
import org.apache.mahout.cf.taste.model.DataModel;
import org.apache.mahout.cf.taste.recommender.RecommendedItem;
import org.apache.mahout.cf.taste.recommender.Recommender;
import org.apache.mahout.cf.taste.similarity.ItemSimilarity;
import org.apache.mahout.common.RandomUtils;

import java.io.*; 
import java.util.List;


public class ItemBasedRecommender implements IRecommender{
	private DataModel model;
	private ItemSimilarity itemSimilarity;
	private Recommender recommender;
	
	private DataModel buildModel(String filePath) throws IOException{
		DataModel model = new FileDataModel (new File(filePath));
		return model;
	}
	
	private ItemSimilarity similarityFactory(Similarity simType) throws TasteException{
		ItemSimilarity similarity;
		if(simType == Similarity.PEARSON){
			similarity = new PearsonCorrelationSimilarity(this.model);
		}else if(simType==Similarity.TANIMOTO){
			similarity =  new TanimotoCoefficientSimilarity(this.model);
		}else if(simType == Similarity.LOGLIKELIHOOD){
			similarity =  new LogLikelihoodSimilarity(this.model);
		}else{
			similarity = new EuclideanDistanceSimilarity(this.model);
		}
		return similarity;
	}
	
	private Recommender buildRecommender(){
		Recommender recommender = new GenericItemBasedRecommender(this.model, this.itemSimilarity);
		return recommender;	
	}
	
	public ItemBasedRecommender(String filePath,Similarity simType) throws IOException, TasteException{
		this.model=buildModel(filePath);
		this.itemSimilarity = similarityFactory(simType);
		this.recommender = buildRecommender();
	}
	
	@Override
	public List<RecommendedItem> recommend(int uid, int amount) throws TasteException {
		List<RecommendedItem> recommendations = this.recommender.recommend(uid, amount);
		return recommendations;
	}

	@Override
	public String evaluate(String evalType) throws TasteException {
		if(evalType.equals("average")){
			RandomUtils.useTestSeed();
			RecommenderEvaluator evaluator =
					new AverageAbsoluteDifferenceRecommenderEvaluator ();
					RecommenderBuilder builder = new RecommenderBuilder() { 
						@Override
				public Recommender buildRecommender(DataModel model)
						throws TasteException {
					return new GenericItemBasedRecommender(model,itemSimilarity);
				}
			};
			System.out.println(" Average Absolute Difference Recommender Evaluator");
			double score = evaluator.evaluate(builder, null, model, 0.8, 1.0);//Trains with 70% of data; tests with 30%
			System.out.println(score);
			return "average>" + score + "\n";
		}else if(evalType.equals("rms")){
			RandomUtils.useTestSeed();
			RecommenderEvaluator evaluator = new RMSRecommenderEvaluator();
			RecommenderBuilder builder = new RecommenderBuilder() { 
				@Override
				public Recommender buildRecommender(DataModel model)
						throws TasteException {
					return new GenericItemBasedRecommender(model, itemSimilarity);
				}
			};
			System.out.println("RMS Recommender Evaluator");
			double score = evaluator.evaluate(builder, null, this.model, 0.8, 1);//Trains with 90% of data; tests with 10%
			System.out.println(score);
			return "rms>"+score + "\n";
			
		} else if(evalType.equals("stats")){
			RandomUtils.useTestSeed();
			RecommenderIRStatsEvaluator evaluator =
			          new GenericRecommenderIRStatsEvaluator ();
			RecommenderBuilder recommenderBuilder = new RecommenderBuilder() { 
			@Override
			public Recommender buildRecommender(DataModel model){
			return new GenericItemBasedRecommender (model, itemSimilarity); }
			};
			IRStatistics stats = evaluator.evaluate(
			recommenderBuilder, null, model, null, 2, GenericRecommenderIRStatsEvaluator.CHOOSE_THRESHOLD, 1.0);
			System.out.println("Generic Recommender IR Stats Evaluator");
			System.out.println(stats.getPrecision());
			System.out.println(stats.getRecall());
			return "precession>" + stats.getPrecision()+">recall>"+stats.getRecall() + "\n";
		}
		return "error" + "\n";
	}
}
