import org.apache.mahout.cf.taste.recommender.*;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.util.*;

public class MahoutTest {
	private MahoutTest() {
		
	}
	public static void main(String args[]) throws Exception {

		Long start = System.currentTimeMillis();
		String fP1M = "D:/dataset/ml-1m/userItemRating1M.csv";
		String fP100K = "D:/dataset/ml-100k/userItemRating100K.csv";
//		String fP100K = "D:/dataset/ml-100k/userItemRating100KTest.csv";
		String resultFilePath = "result.txt";

		UserBasedRecommender UBrecommender;
		Similarity[] sim = { Similarity.PEARSON,
				Similarity.SPEARSON,
				Similarity.TANIMOTO,
				Similarity.LOGLIKELIHOOD,
				Similarity.EUCLIDEAN};
		StringBuffer res = new StringBuffer();
		System.out.println("Uer Based Recommender\n");
		res.append("Uer Based Recommender\n");
		for (Similarity s : sim) {
			res.append("similarity:" + s+"\n");
			System.out.println("similarity:" + s);
			for (int numOfNerghbor = 10; numOfNerghbor <= 100; numOfNerghbor += 10) {
				UBrecommender = new UserBasedRecommender(fP100K, s, numOfNerghbor);
				System.out.println("numOfNerghbor = "+ numOfNerghbor);
				if (numOfNerghbor == 10 || numOfNerghbor == 100) {
					res.append("numOfNerghbor = " + numOfNerghbor + "\n");
				}
				res.append(UBrecommender.evaluate("average"));
				res.append(UBrecommender.evaluate("rms"));
				res.append(UBrecommender.evaluate("stats"));
			}
		}
		
		Similarity[] sim2 = { Similarity.PEARSON,
				Similarity.TANIMOTO,
				Similarity.LOGLIKELIHOOD,
				Similarity.EUCLIDEAN, };
		ItemBasedRecommender IBrecommender;
		System.out.println("Item Based Recommender\n");
		res.append("Item Based Recommender\n");
		for (Similarity s : sim2) {
			IBrecommender = new ItemBasedRecommender(fP100K, s);
			res.append("similarity:" + s +"\n");
			System.out.println("similarity:" + s);
			res.append(IBrecommender.evaluate("average"));
			res.append(IBrecommender.evaluate("rms"));
			res.append(IBrecommender.evaluate("stats"));
		}		
				
		System.out.println(res.toString());
		try {
			File f = new File(resultFilePath);
			if (!f.exists()) {
				if (!f.createNewFile()) {
					System.out.println("failed to create a new file %d");
				}
			}
			BufferedWriter output = new BufferedWriter(new FileWriter(f));
			output.write(res.toString());
			output.close();			
		} catch (Exception e) {
			e.printStackTrace();
		}		
		Long end = System.currentTimeMillis();
		System.out.println("running time: " + ((end - start)/1000/60.0));
			
		SlopeOnerecommender slopeOne = new SlopeOnerecommender(fP100K);
		System.out.println("slope one\n");
		slopeOne.evaluate("average");
		slopeOne.evaluate("rms");
		
		
		
		UserBasedRecommender UBrecommender = new UserBasedRecommender(fP100K, Similarity.PEARSON, 30);
		List<RecommendedItem> recommendations = UBrecommender.recommend(10, 20);// 
		for (RecommendedItem recommendation : recommendations) {
			System.out.println(recommendation);
		}
		
		System.out.println("item based");
		ItemBasedRecommender IBrecommender = new ItemBasedRecommender(fP100K, Similarity.PEARSON);
		recommendations = IBrecommender.recommend(10, 20);// 
		for (RecommendedItem recommendation : recommendations) {
			System.out.println(recommendation);
		}
		
		
		Long start1 = System.currentTimeMillis();
		UserBasedRecommender UBrecommender = new UserBasedRecommender(fP100K, Similarity.PEARSON, 20);
		UBrecommender.evaluate("average");
		Long end1 = System.currentTimeMillis();
		
		System.out.println("item based");
		Long start2 = System.currentTimeMillis();
		ItemBasedRecommender IBrecommender = new ItemBasedRecommender(fP100K, Similarity.PEARSON);
		IBrecommender.evaluate("average");
		Long end2 = System.currentTimeMillis();
		System.out.println("running time1: " + ((end1 - start1)/1000.0));
		System.out.println("running time2: " + ((end2 - start2)/1000.0));
		
		
		
		
	}
}
