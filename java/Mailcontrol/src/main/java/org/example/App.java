package org.example;

import java.util.Properties;
import javax.mail.Message;
import javax.mail.MessagingException;
import javax.mail.Session;
import javax.mail.Transport;
import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeMessage;

public class App {
    public static void main(String[] args) {
        // Địa chỉ email và mật khẩu của bạn
        String from = "ngochoatbcm@gmail.com";
        String password = "lnwt tvnl ksov yjbl";

        // Địa chỉ email người nhận
        String to = "phamvanba2292019@gmail.com";

        // Thiết lập các thuộc tính của máy chủ email
        Properties props = new Properties();
        props.put("mail.smtp.auth", "true");
        props.put("mail.smtp.starttls.enable", "true");
        props.put("mail.smtp.host", "smtp.gmail.com");
        props.put("mail.smtp.port", "587");

        // Tạo phiên làm việc
        Session session = Session.getInstance(props, new javax.mail.Authenticator() {
            protected javax.mail.PasswordAuthentication getPasswordAuthentication() {
                return new javax.mail.PasswordAuthentication(from, password);
            }
        });

        try {
            // Tạo đối tượng MimeMessage
            Message message = new MimeMessage(session);
            message.setFrom(new InternetAddress(from));
            message.setRecipients(Message.RecipientType.TO, InternetAddress.parse(to));
            message.setSubject("Subject of the email");

            // Nội dung HTML của email
            String htmlContent = "<html><body><h1>Hello, this is a template!</h1></body></html>";

            // Thiết lập nội dung của email là HTML
            message.setContent(htmlContent, "text/html");

            // Gửi email
            Transport.send(message);

            System.out.println("Email sent successfully!");

        } catch (MessagingException e) {
            e.printStackTrace();
        }
    }
}
