package Frontend;

import javax.swing.*;
import java.net.*;
import java.util.*;

public class Main {
    public static void main(String[] args) {
        try {
            // Connect to Python backend
            HttpURLConnection conn = (HttpURLConnection) new URL("http://127.0.0.1:5000/hello").openConnection();
            conn.setRequestMethod("GET");

            // Read response
            Scanner sc = new Scanner(conn.getInputStream());
            String response = sc.useDelimiter("\\A").next(); 
            sc.close();

            // Show popup
            JOptionPane.showMessageDialog(null, response, "Backend Response", JOptionPane.INFORMATION_MESSAGE);

        } catch (Exception e) {
            JOptionPane.showMessageDialog(null, "Error: " + e.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
        }
    }
}
