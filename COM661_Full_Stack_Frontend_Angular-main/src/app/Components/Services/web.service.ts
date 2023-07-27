import { HttpClient, HttpHeaders } from '@angular/common/http'
import { Injectable } from '@angular/core';
import { HelperService } from './helper.service';

@Injectable()
export class WebService {

    top_movies_list: any;

    constructor(private http: HttpClient, private helper: HelperService) { }

    get_movies(page: number, page_size: number) {
        return this.http.get('http://127.0.0.1:5000/api/v1.0/movie?pn=' + page + '&ps=' + page_size)
    }

    get_top_10() {
        return this.http.get('http://127.0.0.1:5000/api/v1.0/movie/popularity')
    }

    get_movie_by_title(title: string) {
        return this.http.get('http://127.0.0.1:5000/api/v1.0/movie/' + title)
    }

    get_movie_by_searh_term(term: string) {
        console.log("Searching For:" + term)
        return this.http.get('http://127.0.0.1:5000/api/v1.0/movie/search?' + term)
    }

    gettop10() {
        return this.http.get(
            'http://127.0.0.1:5000/api/v1.0/movie/popularity')
            .subscribe((response: any) => {
                this.top_movies_list = response['Result'];
            })
    }

    getPoster(title: string) {
        return this.http.get(
            'http://127.0.0.1:5000/api/v1.0/movie/' + title + '/poster')
            .subscribe((response: any) => {
                console.log(response)
            })
    }

    removeMovie(title: string) {

        const httpOptions = {
            headers: new HttpHeaders({
                'x-access-token': this.helper.get_token()
            })
        }

        return this.http.delete(
            'http://127.0.0.1:5000/api/v1.0/movie/' + title, httpOptions)
    }

    postMovie(movie: any, char_list: any = []) {

        let postData = new FormData();

        postData.append("title", movie.title_field)
        postData.append("language", movie.language_field)
        postData.append("overview", movie.overview_field)
        postData.append("popularity", movie.popularity_field)
        postData.append("release_date", movie.release_field)
        postData.append("production_companies", movie.companies_field)
        postData.append("genres", movie.genres_field)
        postData.append("keywords", movie.keywords_field)
        postData.append("characters", char_list.toString())
        postData.append("poster", movie.poster_field)

        const httpOptions = {
            headers: new HttpHeaders({
                'x-access-token': this.helper.get_token()
            })
        }

        return this.http.post('http://127.0.0.1:5000/api/v1.0/movie', postData, httpOptions)
    }

    postReview(review: any, title: string) {

        let user_id = this.helper.get_user_id()
        let postData = new FormData();

        postData.append("name", review.name_field)
        postData.append("comment", review.comment_field)
        postData.append("overall", review.rating_field)

        const httpOptions = {
            headers: new HttpHeaders({
                'x-access-token': this.helper.get_token()
            })
        }

        return this.http.post('http://127.0.0.1:5000/api/v1.0/movie/reviews/' + title + '/' + user_id, postData, httpOptions)
    }

    updateMovie(movie: any, title: string, method: string) {
        let postData = new FormData();
        const httpOptions = {
            headers: new HttpHeaders({
                'x-access-token': this.helper.get_token()
            })
        }

        postData.append("title", movie['title'])
        postData.append("language", movie['language'])
        postData.append("overview", movie['overview'])
        postData.append("popularity", movie['popularity'])
        postData.append("release_date", movie['release'])
        postData.append("production_companies", movie['companies'])
        postData.append("genres", movie['genres'])
        postData.append("keywords", movie['keywords'])
        postData.append("characters", movie['characters'])
        postData.append("poster", movie['poster'])

        if (method == 'PUT') {
            return this.http.put('http://127.0.0.1:5000/api/v1.0/movie/' + title, postData, httpOptions)
        }
        return this.http.patch('http://127.0.0.1:5000/api/v1.0/movie/' + title, postData, httpOptions)
    }

    removeReview(title: string) {
        let user_id = this.helper.get_user_id()

        const httpOptions = {
            headers: new HttpHeaders({
                'x-access-token': this.helper.get_token()
            })
        }

        return this.http.delete('http://127.0.0.1:5000/api/v1.0/movie/reviews/' + title + '/' + user_id, httpOptions)
    }

    getCommentByTitle(title: string, user_id: string) {

        const httpOptions = {
            headers: new HttpHeaders({
                'x-access-token': this.helper.get_token()
            })
        }

        return this.http.get('http://127.0.0.1:5000/api/v1.0/movie/reviews/' + title + '/' + user_id, httpOptions)
    }

    updateCommentByTitle(title: string, user_id: string, name: string, comment: string, overview: string) {

        let postData = new FormData();
        postData.append("name", name)
        postData.append("comment", comment)
        postData.append("overview", overview)

        const httpOptions = {
            headers: new HttpHeaders({
                'x-access-token': this.helper.get_token()
            })
        }

        return this.http.patch('http://127.0.0.1:5000/api/v1.0/movie/reviews/' + title + '/' + user_id, postData, httpOptions)
    }

    postMovieToWatchlist(user_id: string, title: string) {

        let postData = new FormData();

        const httpOptions = {
            headers: new HttpHeaders({
                'x-access-token': this.helper.get_token()
            })
        }

        return this.http.post('http://127.0.0.1:5000/api/v2.0/movie/' + title + '/' + user_id, postData, httpOptions)
    }

    getUserWatchlist(user_id: string) {

        const httpOptions = {
            headers: new HttpHeaders({
                'x-access-token': this.helper.get_token()
            })
        }

        return this.http.get('http://127.0.0.1:5000/api/v2.0/movie/' + user_id, httpOptions)
    }

    removeItemFromWatchlist(user_id: string, title: string) {

        const httpOptions = {
            headers: new HttpHeaders({
                'x-access-token': this.helper.get_token()
            })
        }

        return this.http.delete('http://127.0.0.1:5000/api/v2.0/movie/' + title + '/' + user_id, httpOptions)

    }

    getDataSetSize() {
        return this.http.get('http://127.0.0.1:5000/api/v1.0/dataset_size')
    }
}