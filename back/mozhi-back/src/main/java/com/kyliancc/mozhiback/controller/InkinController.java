package com.kyliancc.mozhiback.controller;

import com.kyliancc.mozhiback.model.Assessment;
import com.kyliancc.mozhiback.service.AssessService;
import com.kyliancc.mozhiback.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
public class InkinController {
    private final AssessService assessService;
    private final UserService userService;

    @Autowired
    public InkinController(AssessService assessService, UserService userService) {
        this.assessService = assessService;
        this.userService = userService;
    }

    @RequestMapping("/getToken")
    @CrossOrigin
    public int getToken() {
        return userService.createUser();
    }

    @RequestMapping("/verify")
    @CrossOrigin
    public ResponseEntity<Object> verify(@RequestBody Map<String, Object> data) {
        int token = (int) data.get("token");

        Integer id = userService.getIdByToken(token);

        Map<String, Boolean> responseData = new HashMap<>();

        if (id == null) {
            responseData.put("verified", false);
            return new ResponseEntity<>(responseData, HttpStatus.OK);
        }
        responseData.put("verified", true);
        return new ResponseEntity<>(responseData, HttpStatus.OK);
    }

    @RequestMapping("/upload")
    @CrossOrigin
    public ResponseEntity<Object> uploadImage(MultipartFile file, @RequestParam("token") int token) {
//        MultipartFile file = (MultipartFile) data.get("file");
//        int token = (int) data.get("token");

        Integer id = userService.getIdByToken(token);
        if (id == null) {
            return new ResponseEntity<>(HttpStatus.UNAUTHORIZED);
        }
        assessService.upload(file, id);
        userService.updateUser(id);
        return new ResponseEntity<>(HttpStatus.OK);
    }


    @RequestMapping("/getImage")
    public ResponseEntity<byte[]> getImage(@RequestParam("id") int id) {
        byte[] image = assessService.getImage(id);
        HttpHeaders getImageHeaders = new HttpHeaders();
        getImageHeaders.setContentType(MediaType.IMAGE_PNG);
        return new ResponseEntity<>(image, getImageHeaders, HttpStatus.OK);
    }


    @RequestMapping("/queryAll")
    @CrossOrigin
    public ResponseEntity<List<Assessment>> queryAll(@RequestParam("token") int token) {
        Integer id = userService.getIdByToken(token);
        if (id == null) {
            return new ResponseEntity<>(HttpStatus.UNAUTHORIZED);
        }

        List<Assessment> assessments = assessService.queryAll(id);
        userService.updateUser(id);
        return new ResponseEntity<>(assessments, HttpStatus.OK);
    }

    @RequestMapping("queryInfo")
    @CrossOrigin
    public ResponseEntity<Assessment> queryInfo(@RequestParam("char") String charName) {
        Assessment assessment = assessService.getInfo(charName);
        return new ResponseEntity<>(assessment, HttpStatus.OK);
    }
}
