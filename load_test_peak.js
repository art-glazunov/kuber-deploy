import http from 'k6/http';
import { check, group, sleep } from 'k6';

export const options = {
	  vus: 150,
	  duration: '10s',
	};


export default function () {
    group('API check', () => {
        const response = http.get('http://localhost:4000');
        check(response, {
            "status code should be 200": res => res.status === 200,
        });
        sleep(4);
    });
    group('Check neg response', () => {
        const response = http.post('http://localhost:4000',
                {
                    "text": "ужасно"
                }
        );
        check(response, {
            "status code should be 200": res => res.status === 200,
        });
        check(response, {
            'Service works': (res) => JSON.stringify(res).includes('Отзыв отрицательный'),
          });
        sleep(4);
    });
    group('Check pos response', () => {
        const response = http.post('http://localhost:4000',
                {
                    "text": "отлично"
                }
        );
        check(response, {
            "status code should be 200": res => res.status === 200,
        });
        check(response, {
            'Service works': (res) => JSON.stringify(res).includes('Отзыв положительный'),
          });
        sleep(4);
    });
    group('model info check', () => {
        const response = http.get('http://localhost:4000/model');
        check(response, {
            "status code should be 200": res => res.status === 200,
        });
        check(response, {
            'Get prep info': (res) => JSON.stringify(res).includes('TfidfVectorizer(min_df=10, ngram_range=(1, 3))'),
          });
        check(response, {
            'Get model info': (res) => JSON.stringify(res).includes('LogisticRegression(C=6, random_state=42)'),
          });
        sleep(4)
    });
};