import { Component, ViewEncapsulation, Input } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { WebService } from '../Services/web.service';
import { FormBuilder, Validators } from '@angular/forms';

@Component({
  selector: 'app-movie-form',
  templateUrl: './movie-form.component.html',
  styleUrls: ['./movie-form.component.css'],
})
export class MovieFormComponent {

  is_empty_value = true
  @Input() movie: any;
  is_edit: boolean = false;
  movies_list: any = [];
  movieForm: any;
  movieForm_edit: any;

  char_error: boolean = false

  char_list = []
  character_list: any = []

  constructor(public webService: WebService,
    private router: Router, private route: ActivatedRoute,
    private formBuilder: FormBuilder) {}

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

    is_empty() {

      if (this.char_list.length === 0) {
        return true
      } else
      return false
    }

    add_characters(){

      let actor: any = document.getElementById('actor_field') as HTMLInputElement | null;
      let character: any = document.getElementById('character_field') as HTMLInputElement | null;

      if (actor?.value && character?.value){

        actor = String(actor.value)
        character = character.value

        this.character_list = this.char_list
        let new_values: any = { [actor] : character}
        this.character_list.unshift(new_values)

        this.char_list = this.character_list
        console.log(this.character_list)

        this.is_empty_value = this.is_empty()

      } else {
        // error
        this.char_error = true;
      }

    }

    public remove_characters() {
      this.character_list = this.char_list
      this.character_list.shift()
      this.char_list = this.character_list
      this.is_empty_value = this.is_empty()
    }

  ngOnInit() {

    this.movieForm = this.formBuilder.group({
      title_field: ['', Validators.required],
      language_field: ['', Validators.required],
      overview_field: ['', Validators.required],
      popularity_field: ['', Validators.required],
      release_field: ['', Validators.required],
      companies_field: ['', Validators.required],
      genres_field: ['', Validators.required],
      keywords_field: ['', Validators.required],
      characters_field: [''],
      actor_field: [''],
      poster_field: ['', Validators.required]
      });

    this.movieForm_edit = this.formBuilder.group({
        title_field_edit: ['', Validators.required],
        language_field_edit: ['', Validators.required],
        overview_field_edit: ['', Validators.required],
        popularity_field_edit: ['', Validators.required],
        release_field_edit: ['', Validators.required],
        companies_field_edit: ['', Validators.required],
        genres_field_edit: ['', Validators.required],
        keywords_field_edit: ['', Validators.required],
        characters_field_edit: ['', Validators.required],
        poster_field_edit: ['', Validators.required]
        });

    let title_snap = this.route.snapshot.params['title']

    if (title_snap != undefined) {
      // Edit Movie.
      this.is_edit = true
      this.movies_list = this.webService.get_movie_by_title(this.route.snapshot.params['title'])
    }
      // else - we are going to add a new movie
  }


  isInvalid(control: any) {
    return this.movieForm.controls[control].invalid &&
    this.movieForm.controls[control].touched;
  }

  getFormValues() {
    const title = (<HTMLInputElement>document.getElementById('title_field_edit')).value;
    const language = (<HTMLInputElement>document.getElementById('language_field_edit')).value;
    const overview = (<HTMLInputElement>document.getElementById('overview_field_edit')).value;
    const popularity = (<HTMLInputElement>document.getElementById('popularity_field_edit')).value;
    const release = (<HTMLInputElement>document.getElementById('release_field_edit')).value;
    const companies = (<HTMLInputElement>document.getElementById('companies_field_edit')).value;
    const genres = (<HTMLInputElement>document.getElementById('genres_field_edit')).value;
    const keywords = (<HTMLInputElement>document.getElementById('keywords_field_edit')).value;
    const characters = (<HTMLInputElement>document.getElementById('characters_field_edit')).value;
    const poster = (<HTMLInputElement>document.getElementById('poster_field_edit')).value;

    let obj = {
      'title' : title,
      'language' : language,
      'overview' : overview,
      'popularity' : popularity,
      'release' : release,
      'companies' : companies,
      'genres' : genres,
      'keywords' : keywords,
      'characters' : characters,
      'poster' : poster
    }

    return obj;
  }

  fieldsValid(myDictionary: any) {
    for (let key in myDictionary) {
      let value = myDictionary[key];
      console.log(value)
      if (value == "") {
        return false;
      }
  }
    return true;
  }

  onSubmit_edit(title:string) {
    let values = this.getFormValues()

    const checkbox = document.getElementById('edit_check_box') as HTMLInputElement | null;

    let method = 'PATCH'
    let complete = true
    if (checkbox?.checked == false) {
      if (this.fieldsValid(values) == false) {
        window.alert("All Fields Must Be Filled In!")
        complete = false;
      } else {
        method = 'PUT'
      }
    }

    this.webService.updateMovie(values, title, method).subscribe(
      (response: any) => {
        console.log(response)
    },
    error => window.alert(error))

    if (complete == true) {
      this.router.navigate(['/movie/' + title])
    }
  }

  convert_to_string(){

    let complete_string: string = ""
    for (let x = 0; x < this.char_list.length; x++) {
      if (x != 0) {
        complete_string = complete_string + ','  + JSON.stringify(this.char_list[x])
      } else {
        // First Value.
        complete_string = JSON.stringify(this.char_list[x])
      }
    }

    return complete_string
  }

  onSubmit() {

    this.webService.postMovie(this.movieForm.value, this.convert_to_string())
      .subscribe(
          (response: any) => {
          this.movieForm.reset();
          window.alert(["New Movie Has Been Added To Collection."]);
          this.router.navigate(['/'])
          },
          error => window.alert(error))
  }

  isUntouched_edit() {
    return this.movieForm.controls.title_field_edit.pristine ||
    this.movieForm.controls.language_field_edit.pristine ||
    this.movieForm.controls.overview_field_edit.pristine ||
    this.movieForm.controls.popularity_field_edit.pristine ||
    this.movieForm.controls.release_field_edit.pristine ||
    this.movieForm.controls.companies_field_edit.pristine ||
    this.movieForm.controls.genres_field_edit.pristine ||
    this.movieForm.controls.keywords_field_edit.pristine ||
    this.movieForm.controls.characters_field_edit.pristine ||
    this.movieForm.controls.poster_field_edit.pristine;
  }

  isIncomplete_edit() {
    return this.isInvalid('title_field_edit') ||
    this.isInvalid('language_field_edit') ||
    this.isInvalid('overview_field_edit') ||
    this.isInvalid('popularity_field_edit') ||
    this.isInvalid('release_field_edit') ||
    this.isInvalid('companies_field_edit') ||
    this.isInvalid('genres_field_edit') ||
    this.isInvalid('keywords_field_edit') ||
    this.isInvalid('characters_field_edit') ||
    this.isInvalid('poster_field_edit') ||
    this.isUntouched();
  }

  isUntouched() {
    return this.movieForm.controls.title_field.pristine ||
    this.movieForm.controls.language_field.pristine ||
    this.movieForm.controls.overview_field.pristine ||
    this.movieForm.controls.popularity_field.pristine ||
    this.movieForm.controls.release_field.pristine ||
    this.movieForm.controls.companies_field.pristine ||
    this.movieForm.controls.genres_field.pristine ||
    this.movieForm.controls.keywords_field.pristine ||
    this.movieForm.controls.poster_field.pristine;
  }

  isIncomplete() {
    return this.isInvalid('title_field') ||
    this.isInvalid('language_field') ||
    this.isInvalid('overview_field') ||
    this.isInvalid('popularity_field') ||
    this.isInvalid('release_field') ||
    this.isInvalid('companies_field') ||
    this.isInvalid('genres_field') ||
    this.isInvalid('keywords_field') ||
    this.isInvalid('poster_field') ||
    this.isUntouched();
  }

  getStringValue(obj: any) {
    let myJSON = JSON.stringify(obj);
    myJSON = myJSON.replaceAll('[', '');
    myJSON = myJSON.replaceAll(']', '');
    myJSON = myJSON.replaceAll('/', '');
    myJSON = myJSON.replaceAll('\\', '');
    return myJSON
  }

}