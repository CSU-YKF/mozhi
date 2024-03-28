package com.kyliancc.mozhiback.service;

import com.kyliancc.mozhiback.repository.UserMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Random;

@Service
public class UserService {
    private UserMapper repository;
    private Random random;

    @Autowired
    public UserService(UserMapper repository) {
        this.repository = repository;
        random = new Random();
    }

    public Integer getIdByToken(int token) {
        return repository.queryIdByToken(token);
    }

    public int createUser() {
        int token = 0;
        while (true) {
            int randInt = random.nextInt(0, Integer.MAX_VALUE);
            if (getIdByToken(token) == null) {
                token = randInt;
                break;
            }
        }

        repository.insertUser(token);
        return token;
    }

    public void updateUser(int id) {
        repository.updateUserLastActive(id);
    }
}
