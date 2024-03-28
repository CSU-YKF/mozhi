package com.kyliancc.mozhiback.service;

import com.kyliancc.mozhiback.client.AlgorithmServiceClient;
import com.kyliancc.mozhiback.model.Assessment;
import com.kyliancc.mozhiback.repository.AssessMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.Base64;
import java.util.List;

@Service
public class AssessService {
    private final AlgorithmServiceClient client;
    private final AssessMapper repository;

    @Autowired
    public AssessService(AlgorithmServiceClient client, AssessMapper repository) {
        this.client = client;
        this.repository = repository;
    }

    public void upload(MultipartFile file, int userId) {
        String base64String = null;
        try {
            byte[] imgBytes = file.getBytes();
            base64String = Base64.getEncoder().encodeToString(imgBytes);
        } catch (IOException e) {
            e.printStackTrace();
        }

        if (base64String == null) {
            throw new RuntimeException();
        }

        Assessment assessment = client.evaluate(base64String);
        assessment.setImageData(base64String);

        repository.insertAssess(
                userId,
                base64String,
                assessment.getScore(),
                assessment.getComment(),
                assessment.getCharName()
        );
    }

    public byte[] getImage(int assessId) {
        String imageData = repository.queryImageDataById(assessId);
        return Base64.getDecoder().decode(imageData);
    }

    public List<Assessment> queryAll(int userId) {
        return repository.queryIdByUserId(userId);
    }

    public Assessment getInfo(String charName) {
        return client.getInfo(charName);
    }
}
