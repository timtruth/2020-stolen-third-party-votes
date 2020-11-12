package mainpckge;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Iterator;

import org.json.JSONArray;
import org.json.JSONObject;

public class NYT3rdPartySteal {
	public static void main(String[] args) throws IOException {
		String nytDataFolder = "C:\\Users\\TimTruth\\Documents\\VoterFraud\\NYTTmeSeries";
		File dir = new File(nytDataFolder);
		File[] directoryListing = dir.listFiles();
		double totalStolenVotes = 0;
		if (directoryListing != null) {
		    for (File f : directoryListing) {
		    	String fName = f.getAbsolutePath();
				String contents = new String(Files.readAllBytes(Paths.get(fName)));
				JSONObject jsonObject = new JSONObject(contents.trim());
				JSONArray raceObjs = jsonObject.getJSONObject("data").getJSONArray("races");
				for(int i = 0; i < raceObjs.length(); i++) {
					JSONObject race = (JSONObject) raceObjs.get(i);
					if(race.getString("race_type").equals("president")) {
						JSONArray timeseriesData = race.getJSONArray("timeseries");
						double totalStateLost3rdPartyVotes = 0; 
						String state = race.getString("state_name");
						System.out.println("***" + state + "***");
						double lastVotes3rd = 0;
						for(int j = 0; j < timeseriesData.length(); j++) {
							JSONObject tsPnt = timeseriesData.getJSONObject(j);
							JSONObject voteShares = tsPnt.getJSONObject("vote_shares");
							double percD = voteShares.getDouble("bidenj");
							double percR = voteShares.getDouble("trumpd");
							double totalVotes = tsPnt.getDouble("votes");
							String ts = tsPnt.getString("timestamp");
							double perc3rd = 1.0 - percD - percR;
					        double votesDem = totalVotes * percD;
					        double votesRep = totalVotes * percR;
					        double votes3rd = totalVotes * perc3rd;
					        double gainedVotes = votes3rd - lastVotes3rd;
					        if(gainedVotes < -1) {
					        	double numVotes = Math.abs(Math.round(gainedVotes * 100.0) / 100.0);
					        	totalStateLost3rdPartyVotes += numVotes;
					        	System.out.println("3rd Party Candidate(s) LOSE " + numVotes + " votes (From " + (Math.round(lastVotes3rd * 100.0) / 100.0) + " to " + (Math.round(votes3rd * 100.0) / 100.0) + ") At " + ts);
					        }
					        lastVotes3rd = votes3rd;
						}
						if(totalStateLost3rdPartyVotes > 0) {
							totalStolenVotes += totalStateLost3rdPartyVotes;
							System.out.println(state + " Lost " + totalStateLost3rdPartyVotes + " 3rd Party Votes");
						}
					}
				}
		    }
		}
		System.out.println("Total 3rd party votes lost/stolen: " + totalStolenVotes);
    }
}
