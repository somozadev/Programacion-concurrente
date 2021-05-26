import java.io.IOException;
import java.util.regex.Pattern;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class WordCounterMapper extends Mapper<LongWritable, Text, Text, IntWritable> {

	private final static IntWritable one = new IntWritable(1);
	private final static Pattern SPLIT_PATTERN = Pattern.compile("\\s*\\b\\s*");
	
  @Override
  public void map(LongWritable key, Text value, Context context)
      throws IOException, InterruptedException {

    String line = value.toString();
    line = line.replaceAll("[^a-zA-Z0-9 ]","").toLowerCase();
    Text currentWord = new Text();
    
    String words[] = SPLIT_PATTERN.split(line);
    
    for(int i = 0; i < words.length; i++)
    	
    {
    	if(words[i].isEmpty())
    	{
    		continue;
    	}
    	currentWord = new Text(words[i]);
    	context.write(currentWord, one);
    }

  }
}
