import org.apache.mahout.cf.taste.impl.model.file.*;  
import org.apache.mahout.cf.taste.impl.neighborhood.*;  
import org.apache.mahout.cf.taste.impl.recommender.*;  
import org.apache.mahout.cf.taste.impl.similarity.*;  
import org.apache.mahout.cf.taste.model.*;  
import org.apache.mahout.cf.taste.neighborhood.*;  
import org.apache.mahout.cf.taste.recommender.*;  
import org.apache.mahout.cf.taste.similarity.*;  
import java.io.*;  
import java.util.*;  
public class RecommenderIntro {  
    private RecommenderIntro(){};  
      
    public static void main (String args[])throws Exception{  
                // step:1 构建模型 2 计算相似度 3 查找k紧邻 4 构造推荐引擎
//    	String fileName = "D:/ws2/MovieRecommonderMahout/csvFiles/userItemRating.csv";
    	String fileName = "D:/ws2/MovieRecommonder/datasetCSV/userItemRating.csv";
//    	String fileName = "D:/ws2/MovieRecommonderMahout/inputData/demotest.txt";
        DataModel  model =new FileDataModel(new File(fileName));
        UserSimilarity similarity =new PearsonCorrelationSimilarity(model);  
        UserNeighborhood neighborhood =new NearestNUserNeighborhood(2,similarity,model);  
        Recommender recommender= new GenericUserBasedRecommender(model,neighborhood,similarity);  
        List<RecommendedItem> recommendations =recommender.recommend(1, 2);//为用户1推荐两个ItemID  
        for(RecommendedItem recommendation :recommendations){  
            System.out.println(recommendation);  
        }            
    }  
}  