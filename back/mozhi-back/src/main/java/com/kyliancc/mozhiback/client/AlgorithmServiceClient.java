package com.kyliancc.mozhiback.client;

import com.kyliancc.mozhiback.model.Assessment;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.Map;

@Component
public class AlgorithmServiceClient {
    private final RestTemplate template;

    public AlgorithmServiceClient() {
        template = new RestTemplate();
    }

    public Assessment evaluate(String b64Str) {
        String url = "http://localhost:50051/evaluate";

        Map<String, String> data = new HashMap<>();
        data.put("image_base64", b64Str);

        return template.postForObject(url, data, Assessment.class);
    }

    public Assessment getInfo(String charName) {
        String url = "http://localhost:50051/get_info?char=" + charName;

        return template.getForObject(url, Assessment.class);
    }
}
