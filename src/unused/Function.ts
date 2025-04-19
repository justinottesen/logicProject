export class Function {
    text: string
    // rule:  //create rule type
    parents: number[]
    constructor(text: string, parents: number[]) {
        this.text = text
        this.parents = []
    }

    addParent(parent: number) {
        this.parents.push(parent)
    }
    removeParent(parent: number) {
        this.parents.splice(this.parents.indexOf(parent), 1)
    }



}