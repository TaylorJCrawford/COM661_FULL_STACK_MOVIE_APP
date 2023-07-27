import { Component } from '@angular/core';
import { ReviewCardComponent } from '../review-card/review-card.component';
import { ActivatedRoute } from '@angular/router';
import { WebService } from '../Services/web.service';
import { Router } from '@angular/router';
import { HelperService } from '../Services/helper.service';
import { FormBuilder, Validators } from '@angular/forms';
import { CharacterCardsComponent } from '../character-cards/character-cards.component';
@Component({
  selector: 'app-movie',
  templateUrl: './movie.component.html',
  styleUrls: ['./movie.component.css'],
})
export class MovieComponent {
  movie_list: any;
  is_admin: boolean = false;
  user_id: string = "";
  display_add_comment: string = "none";
  reviewForm: any;
  watchlist_button = true;

  page_size: number = 6
  page: number = 1;
  totalRecords = 20;

  constructor(private webService: WebService,
    private helper: HelperService,
    private route: ActivatedRoute,
    private router: Router,
    private formBuilder: FormBuilder) { }

  ngOnInit() {

    this.reviewForm = this.formBuilder.group({
      name_field: ['', Validators.required],
      comment_field: ['', Validators.required],
      rating_field: ['3', Validators.required]
    });

    let title = this.route.snapshot.params['title'];
    this.movie_list = this.webService.get_movie_by_title(title)
    this.is_admin = this.helper.is_admin();
    this.user_id = this.helper.get_user_id();
    this.movie_list.subscribe(
      (response: any) => {
        this.totalRecords = response[0].reviews.length;
      },
    )

    this.webService.getUserWatchlist(this.user_id).subscribe(
      (response: any) => {
        for (let x = 0; x < response[0].length; x++) {
          if (response[0][x]['title'] == title) {
            this.watchlist_button = false;
            break;
          }
        }
      }
    )
  }

  pagination(event: any) {
    console.log(event)
    this.page = event
    sessionStorage['page'] = this.page;
  }

  onSubmit(title: string) {

    this.webService.postReview(this.reviewForm.value, title)
      .subscribe(
        (response: any) => {
          this.reviewForm.reset();
          window.alert([response.Message]);
          this.addComment()
          this.movie_list = this.webService.get_movie_by_title(this.route.snapshot.params['title'])
        },
        error => window.alert("You may only add one review to a movie."))
  }

  clear_comment() {
    (<HTMLInputElement>document.getElementById('name_field')).value = "";
    (<HTMLInputElement>document.getElementById('comment_field')).value = "";
    (<HTMLInputElement>document.getElementById('rating_field')).value = "1";
  }

  isInvalid(control: any) {
    return this.reviewForm.controls[control].invalid &&
      this.reviewForm.controls[control].touched;
  }

  isUntouched() {
    return this.reviewForm.controls.name_field.pristine ||
      this.reviewForm.controls.comment_field.pristine;
  }

  isIncomplete() {
    return this.isInvalid('name_field') ||
      this.isInvalid('comment_field') ||
      this.isUntouched();
  }


  addComment() {
    if (this.display_add_comment == "block") {
      this.display_add_comment = "none";
      (<HTMLInputElement>document.getElementById('add_comment_button')).innerHTML = "Add New Comment";
    } else {
      this.display_add_comment = "block";
      (<HTMLInputElement>document.getElementById('add_comment_button')).innerHTML = "Hide Comment Form";
      (<HTMLInputElement>document.getElementById('add_comment_title')).focus()
    }
  }

  isLogin(): boolean {
    return this.helper.is_token_present()
  }

  sendTo(url: string, movie_pass: any) {
    console.log("SEND TO CALLED")
    console.log(url)
    this.router.navigate([url])
  }

  removeMovie(title: string) {
    this.webService.removeMovie(title)
      .subscribe((response: any) => {
        window.alert([response.Message]);
        this.router.navigate(['/'])
      })
  }

  getChar(obj: any) {
    let myJSON = JSON.stringify(obj);
    try {
      myJSON = myJSON.replaceAll('[', '');
      myJSON = myJSON.replaceAll('{', '');
      myJSON = myJSON.replaceAll(']', '');
      myJSON = myJSON.replaceAll('}', '');
      myJSON = myJSON.replaceAll('/', '');
      myJSON = myJSON.replaceAll('\\', '');
    } catch (e: unknown) {
      console.log(e)
    }
    let arrra_v = myJSON.split(',')
    let result = []
    for (let x = 0; x < arrra_v.length; x++) {
      let tempJson = { 'actor': '', 'character': '' }
      let temp1 = arrra_v[x].split(':');
      try {
        tempJson.actor = temp1[0].replaceAll('"', '');
        tempJson.character = temp1[1].replaceAll('"', '');
      } catch (e: unknown) {
        console.log(e)
      }
      result.push(tempJson)
    }
    return result
  }

  getStringValue(obj: any) {
    let myJSON = JSON.stringify(obj);
    myJSON = myJSON.replaceAll('[', '');
    myJSON = myJSON.replaceAll('{', '');
    myJSON = myJSON.replaceAll(']', '');
    myJSON = myJSON.replaceAll('}', '');
    myJSON = myJSON.replaceAll('/', '');
    myJSON = myJSON.replaceAll('\\', '');
    return myJSON
  }

  stringToList(list: any) {
    let results = []
    for (let x = 0; x < list.length; x++) {
      results.push(list[x])
    }
    return results
  }

  addToWatchlist(title: string) {
    this.webService.postMovieToWatchlist(this.user_id, title).subscribe(
      (response: any) => {
      },
      error => console.log(error))

      window.alert("Movie has been added to your watchlist.")
      window.location.reload()
  }
}
