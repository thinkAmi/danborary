$(document).ready(function() {
  const page = new MenuPage();
  page.initialize();
  page.setFocusToBox();
});


class MenuPage {
  initialize() {
    this.registerEventHandlers();
  }

  registerEventHandlers() {
    const registerButton = $('#register');
    registerButton.on('click', event => {
      this.onClickRegister(event);
    });
    $('#box').on('keypress', event => {
      if (event.keyCode === 13) {
        event.preventDefault();
        registerButton.trigger('click');
      }
    })

    const printButton = $('#print');
    printButton.on('click', event => {
      this.onClickPrint(event);
    });
    $('#start').on('keypress', event => {
      if (event.keyCode === 13) {
        event.preventDefault();
        printButton.trigger('click');
      }
    })
  }

  onClickRegister(event) {
    this.toRegisterPage();
  }

  onClickPrint(event) {
    this.toPrintPage();
  }

  toRegisterPage() {
    const box = $('#box').val();
    if (!box) {
      alert('箱番号は必須です');
      return;
    }
    const url = `/packing/box/${box}/`;
    console.log(url);
    window.location.href = url;
  }

  toPrintPage() {
    const startBox = $('#start').val();
    if (!startBox) {
      alert('開始箱番号は必須です');
      return;
    }
    window.location.href = `/packing/print/start/${startBox}/`;
  }

  setFocusToBox() {
    $('#box').focus();
  }
}
