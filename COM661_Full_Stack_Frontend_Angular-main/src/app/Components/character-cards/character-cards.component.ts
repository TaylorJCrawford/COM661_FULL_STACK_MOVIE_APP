import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-character-cards',
  templateUrl: './character-cards.component.html',
  styleUrls: ['./character-cards.component.css']
})
export class CharacterCardsComponent {

  @Input() Actor: string = "";
  @Input() Character: string = "";

}