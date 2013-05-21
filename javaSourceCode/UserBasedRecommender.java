import java.io.File;
import java.io.IOException;
import java.util.List;

import org.apache.mahout.cf.taste.model.DataModel;
import org.apache.mahout.cf.taste.neighborhood.UserNeighborhood;
import org.apache.mahout.cf.taste.common.TasteException;
import org.apache.mahout.cf.taste.eval.IRStatistics;
import org.apache.mahout.cf.taste.eval.RecommenderBuilder;
import org.apache.mahout.cf.taste.eval.RecommenderEvaluator;
import org.apache.mahout.cf.taste.eval.RecommenderIRStatsEvaluator;
import org.apache.mahout.cf.taste.impl.eval.AverageAbsoluteDifferenceRecommenderEvaluator;
import org.apache.mahout.cf.taste.impl.eval.GenericRecommenderIRStatsEvaluator;
import org.apache.mahout.cf.taste.impl.eval.RMSRecommenderEvaluator;
import org.apache.mahout.cf.taste.impl.model.file.FileDataModel;
import org.apache.mahout.cf.taste.impl.neighborhood.NearestNUserNeighborhood;
import org.apache.mahout.cf.taste.impl.neighborhood.ThresholdUserNeighborhood;
import org.apache.mahout.cf.taste.impl.recommender.GenericUserBasedRecommender;
import org.apache.mahout.cf.taste.impl.similarity.EuclideanDistanceSimilarity;
import org.apache.mahout.cf.taste.impl.similarity.LogLikelihoodSimilarity;
import org.apache.mahout.cf.taste.impl.similarity.SpearmanCorrelationSimilarity;
import org.apache.mahout.cf.taste.impl.similarity.TanimotoCoefficientSimilarity;
import org.apache.mahout.cf.taste.recommender.RecommendedItem;
import org.apache.mahout.cf.taste.recommender.Recommender;
import org.apache.mahout.cf.taste.similarity.UserSimilarity;
import org.apache.mahout.cf.taste.impl.similarity.PearsonCorrelationSimilarity;
import org.apache.mahout.common.RandomUtils;



public class UserBasedRecommender  implements IRecommender{
	private DataModel model;
	private UserSimilarity userSimilarity;
	private UserNeighborhood neighborhood;
	private Recommender recommender;
	
	private DataModel buildModel(String filePath) throws IOException{
		DataModel model = new FileDataModel (new File(filePath));
		return model;
	}
	
	private UserSimilarity similarityFactory(Similarity simType) throws TasteException{
		UserSimilarity similarity;
		if(simType == Similarity.PEARSON){
			similarity = new PearsonCorrelationSimilarity(this.model);
		}else if(simType==Similarity.SPEARSON){
			similarity =  new SpearmanCorrelationSimilarity(this.model);
		}else if(simType==Similarity.TANIMOTO){
			similarity =  new TanimotoCoefficientSimilarity(this.model);
		}else if(simType == Similarity.LOGLIKELIHOOD){
			similarity =  new LogLikelihoodSimilarity(this.model);
		}else{
			similarity = new EuclideanDistanceSimilarity(this.model);
		}
		return similarity;
	}
	
	private UserNeighborhood buildNeighborhood(int numOfNeighbor) throws TasteException{
		UserNeighborhood neighborhood =
			      new NearestNUserNeighborhood(numOfNeighbor, this.userSimilarity, this.model);	
		return neighborhood;
	}
	
	private UserNeighborhood buildNeighborhood(float threshold){
		UserNeighborhood neighborhood =
			      new ThresholdUserNeighborhood(threshold, this.userSimilarity, this.model);	
		return neighborhood;
	}
	
	private Recommender buildRecommender(){
		Recommender recommender = new GenericUserBasedRecommender(this.model,
				this.neighborhood, this.userSimilarity);
		return recommender;	
	}
	
	
	public UserBasedRecommender(String filePath,Similarity simType,int numOfNeighbor) throws IOException, TasteException{
		this.model=buildModel(filePath);
		this.userSimilarity = similarityFactory(simType);
		this.neighborhood = buildNeighborhood(numOfNeighbor);
		this.recommender = buildRecommender();
	}

	public UserBasedRecommender(String filePath,Similarity simType,float threshold) throws IOException, TasteException{
		this.model=buildModel(filePath);
		this.userSimilarity = similarityFactory(simType);
		this.neighborhood = buildNeighborhood(threshold);
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
					return new GenericUserBasedRecommender(model, neighborhood,
							userSimilarity);
				}
			};
			System.out.println("Average Absolute Difference Recommender Evaluator");
			double score = evaluator.evaluate(builder, null, this.model, 0.8, 1);//Trains with 90% of data; tests with 10%
			System.out.println(score);
			return "average>"+score + "\n";
		} else if(evalType.equals("rms")){
			RandomUtils.useTestSeed();
			RecommenderEvaluator evaluator = new RMSRecommenderEvaluator();
			RecommenderBuilder builder = new RecommenderBuilder() { 
				@Override
				public Recommender buildRecommender(DataModel model)
						throws TasteException {
					return new GenericUserBasedRecommender(model, neighborhood,
							userSimilarity);
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
			return new GenericUserBasedRecommender (model, neighborhood, userSimilarity); }
			};
			IRStatistics stats = evaluator.evaluate(
							recommenderBuilder, null,this.model, null, 100, GenericRecommenderIRStatsEvaluator.CHOOSE_THRESHOLD, 1.0);
			System.out.println("Generic Recommender IR Stats Evaluator");
			System.out.println(stats.getPrecision());
			System.out.println(stats.getRecall());
			String res = "precession>" +stats.getPrecision() +">recall>"+stats.getRecall() + "\n"; 
			return res;
		}
		return "error" + "\n";
	}	
}
