import java.io.File;
import java.io.IOException;
import java.util.List;

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
import org.apache.mahout.cf.taste.impl.recommender.slopeone.SlopeOneRecommender;
import org.apache.mahout.cf.taste.model.DataModel;
import org.apache.mahout.cf.taste.recommender.RecommendedItem;
import org.apache.mahout.cf.taste.recommender.Recommender;
import org.apache.mahout.common.RandomUtils;


public class SlopeOnerecommender implements IRecommender{
	private DataModel model;
	private Recommender recommender;
	
	private DataModel buildModel(String filePath) throws IOException{
		DataModel model = new FileDataModel (new File(filePath));
		return model;
	}
	
	public SlopeOnerecommender(String filePath) throws IOException, TasteException{
		this.model=buildModel(filePath);
		this.recommender = new SlopeOneRecommender(this.model);
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
					RecommenderBuilder builder = new RecommenderBuilder() { @Override
				public Recommender buildRecommender(DataModel model)
						throws TasteException {
					return new SlopeOneRecommender(model);
				}
			};
			double score = evaluator.evaluate(builder, null, model, 0.8, 1.0);//Trains with 70% of data; tests with 30%
			System.out.println("Average Absolute Difference Recommender Evaluator");
			System.out.println(score);
			return "average>"+ score+"\n";
		}else if(evalType.equals("rms")){
			RandomUtils.useTestSeed();
			RecommenderEvaluator evaluator = new RMSRecommenderEvaluator();
			RecommenderBuilder builder = new RecommenderBuilder() { 
				@Override
				public Recommender buildRecommender(DataModel model)
						throws TasteException {
					return new SlopeOneRecommender(model);
				}
			};
			System.out.println("RMS Recommender Evaluator");
			double score = evaluator.evaluate(builder, null, this.model, 0.8, 1);//Trains with 80% of data; tests with 10%
			System.out.println(score);
			return "rms>"+score + "\n";			
		} else {
			RandomUtils.useTestSeed();
			RecommenderIRStatsEvaluator evaluator =
			          new GenericRecommenderIRStatsEvaluator ();
			RecommenderBuilder recommenderBuilder = new RecommenderBuilder() { 
			@Override
			public Recommender buildRecommender(DataModel model) throws TasteException{
			return new SlopeOneRecommender(model); }
			};
			IRStatistics stats = evaluator.evaluate(
			recommenderBuilder, null, model, null, 10, GenericRecommenderIRStatsEvaluator.CHOOSE_THRESHOLD, 1.0);
			System.out.println(stats.getPrecision());
			System.out.println(stats.getRecall());
			return "precession>" + stats.getPrecision()+">recall>"+stats.getRecall() + "\n";
		}
	}

}
