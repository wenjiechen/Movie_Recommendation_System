
import java.io.*;

public class FileWriting{

public static void main(String[] args) {
      write("123.txt", "hello");
}

public static void write(String path, String content) {
      String s = new String();
      String s1 = new String();
		try {
			File f = new File(path);
			if (!f.exists()) {
				if (!f.createNewFile()) {
					System.out.println("failed to create a new file %d");
				}
			}

       BufferedReader input = new BufferedReader(new FileReader(f));
       
       while ((s = input.readLine()) != null) {
        s1 += s + "\n";
       }
       System.out.println("文件内容：" + s1);
       input.close();
       
       s1 += content;
       Double d = 99.99;
       String figure = d.toString();
       BufferedWriter output = new BufferedWriter(new FileWriter(f));
       output.write(content);
       output.write("\ntest");
       output.write(figure);
       output.close();
      } catch (Exception e) {
       e.printStackTrace();
      }
}
}
