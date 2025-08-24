package Frontend;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        try {
            URL url = new URL("http://127.0.0.1:5000/attendance/list");
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");

            InputStream inputStream = conn.getInputStream();
            Scanner sc = new Scanner(inputStream).useDelimiter("\\A");
            String response = sc.hasNext() ? sc.next() : "";
            sc.close();

            // Remove the outer braces {"attendance":[...]} to parse manually
            String arrayContent = response
                    .replaceFirst("^\\s*\\{\\s*\"attendance\"\\s*:\\s*\\[", "")
                    .replaceFirst("]\\s*}\\s*$", "");

            String[] entries = arrayContent.split("\\},\\{");
            for (int i = 0; i < entries.length; i++) {
                entries[i] = entries[i].replaceAll("^\\{", "").replaceAll("}$", "");
            }

            String[] columns = {"First", "Last", "Age", "Dropped Off", "Picked Up", "Emergency Contact Name", "Emergency Contact Phone"};
            DefaultTableModel tableModel = new DefaultTableModel(columns, 0);

            for (String entry : entries) {
                String[] fields = new String[columns.length];
                String[] pairs = entry.split(",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)");

                for (String pair : pairs) {
                    String[] keyValue = pair.split(":", 2);
                    if (keyValue.length < 2) continue;
                    String key = keyValue[0].trim().replaceAll("^\"|\"$", "");
                    String value = keyValue[1].trim().replaceAll("^\"|\"$", "");
                    switch (key) {
                        case "First": fields[0] = value; break;
                        case "Last": fields[1] = value; break;
                        case "Age": fields[2] = value; break;
                        case "Dropped_off": fields[3] = value; break;
                        case "Picked_up": fields[4] = value; break;
                        case "Emergency_Contact_Name": fields[5] = value; break;
                        case "Emergency_Contact_Phone": fields[6] = value; break;
                    }
                }
                tableModel.addRow(fields);
            }

            JTable table = new JTable(tableModel);
            table.setFillsViewportHeight(true);
            JScrollPane scrollPane = new JScrollPane(table);

            JFrame frame = new JFrame("Attendance List");
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            frame.add(scrollPane);
            frame.setSize(800, 400);
            frame.setLocationRelativeTo(null);
            frame.setVisible(true);

        } catch (Exception e) {
            e.printStackTrace();
            JOptionPane.showMessageDialog(null, "Error: " + e.getMessage());
        }
    }
}
