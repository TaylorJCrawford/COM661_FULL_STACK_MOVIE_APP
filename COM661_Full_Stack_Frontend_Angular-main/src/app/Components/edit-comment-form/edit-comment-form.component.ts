import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { WebService } from '../Services/web.service';

@Component({
  selector: 'app-edit-comment-form',
  templateUrl: './edit-comment-form.component.html',
  styleUrls: ['./edit-comment-form.component.css']
})
export class EditCommentFormComponent {

  title: string = "";
  user_id: string = "";
  name: string = "";
  comment: string = "";
  rating: string = "";

  constructor(private webService: WebService,
    private router: Router,
    private route: ActivatedRoute) { }


  ngOnInit() {

    this.title = this.route.snapshot.params['title']
    this.user_id = this.route.snapshot.params['comment_id']

    this.webService.getCommentByTitle(this.title, this.user_id).subscribe(
      (response: any) => {

        for (let result of response['Result'][0]['reviews']) {
          if (result['user_id'] == this.user_id) {
            this.name = result['name']
            this.comment = result['comment']
            this.rating = result['overview']
          }
        }

        (<HTMLInputElement>document.getElementById('name_field')).value = this.name;
        (<HTMLInputElement>document.getElementById('comment_field')).value = this.comment;
        (<HTMLInputElement>document.getElementById('rating_field' + String(this.rating))).checked = true;

      },
      error => window.alert("You may only add one review to a movie."))
  }

  setRadio(element: string) {
    let element_num = Number(element) - 1
    let values = ['1', '2', '3', '4', '5'];
    values.splice(element_num, 1);

    for (var item of values) {
      (<HTMLInputElement>document.getElementById('rating_field' + item)).checked = false;
    }
    (<HTMLInputElement>document.getElementById('rating_field' + element)).checked = true;
  }

  getCheckValue() {
    if ((<HTMLInputElement>document.getElementById('rating_field1')).checked) {
      return '1'
    } else if ((<HTMLInputElement>document.getElementById('rating_field2')).checked) {
      return '2'
    } else if ((<HTMLInputElement>document.getElementById('rating_field3')).checked) {
      return '3'
    } else if ((<HTMLInputElement>document.getElementById('rating_field4')).checked) {
      return '4'
    }
    return '5'
  }

  updateComment() {
    let new_name = (<HTMLInputElement>document.getElementById('name_field')).value
    let new_comment = (<HTMLInputElement>document.getElementById('comment_field')).value
    let rating = this.getCheckValue()
    this.webService.updateCommentByTitle(this.title, this.user_id, new_name, new_comment, rating)
      .subscribe(
        (response: any) => {
        },
        error => window.alert("You may only add one review to a movie."))
    this.router.navigate(['/movie/', this.title])
  }
}
