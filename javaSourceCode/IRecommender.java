import org.apache.mahout.cf.taste.common.TasteException;
import org.apache.mahout.cf.taste.recommender.RecommendedItem;
import java.util.List;

public interface IRecommender {
	public  List<RecommendedItem> recommend(int uid,int amount) throws TasteException;
	
	public String evaluate(String evalType)throws TasteException;
}
