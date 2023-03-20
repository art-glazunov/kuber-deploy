import http from 'k6/http';
import { check, group, sleep } from 'k6';

export let options = {
    stages: [
        { duration: '5s', target: 50 }, 
        { duration: '5s', target: 100}, 
        { duration: '5s', target: 300 }, 
        { duration: '20s', target: 600 }, 
        { duration: '5s', target: 300}, 
        { duration: '5s', target: 200 }, 
        { duration: '10s', target: 0 }, 
      ],
};

export default function () {
    group('API check', () => {
        const response = http.get('http://localhost:4000');
        check(response, {
            "status code should be 200": res => res.status == 200,
        });
        sleep(4);
    });
    group('Check neg response', () => {
        const response = http.post('http://localhost:4000/',
                {
                    "text": "ужасно"
                }
        );
        check(response, {
            "status code should be 200": res => res.status == 200,
        });
        check(response, {
            'Service works': (res) => JSON.stringify(res).includes('Отзыв отрицательный'),
          });
        sleep(4);
    });
    group('Check pos response', () => {
        const response = http.post('http://localhost:4000/',
                {
                    "text": "отлично"
                }
        );
        check(response, {
            "status code should be 200": res => res.status == 200,
        });
        check(response, {
            'Service works': (res) => JSON.stringify(res).includes('Отзыв положительный'),
          });
        sleep(4);
    });
};