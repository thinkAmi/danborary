$(document).ready(function() {
  const page = new PackingPage();
  page.initialize();
  page.setFocusToKey();
});


class PackingPage {
  constructor() {
    this.dataTable = null;
  }

  initialize() {
    this.registerEventHandlers();
    this.loadDataTables();
  }

  registerEventHandlers() {
    const searchButton = $('#search');
    searchButton.on('click', event => {
      this.onClickSearch(event);
    });

    $('#key').on('keypress', event => {
      if (event.keyCode === 13) {
        event.preventDefault();
        searchButton.trigger('click');
      }
    })

    $('#register').on('click', event => {
      this.onClickRegister(event);
    });
  }

  onClickSearch(event) {
    this.setValuesFromNdl();
  }

  onClickRegister(event) {
    this.registerBook();
  }

  setValuesFromNdl() {
    this.setSpinner('search');

    $.ajax({
      url: '/api/ndl/',
      method: 'GET',
      timeout: 10000,
      dataType: 'json',
      data: {key: $('#key').val()},
    }).then(
      data => {
        this.removeSpinner('search');

        $('#isbn').val(data.isbn);
        $('#title').val(data.title);
        $('#creator').val(data.creator);
        $('#publisher').val(data.publisher);

        $('#register').focus();
      },
      () => {
        this.removeSpinner();
        this.clearFields();
      }
    )
  }

  registerBook() {
    const title = $('#title').val();
    if (!title) {
      alert('タイトルは必須です');
      return;
    }

    this.setSpinner('register')

    const params = {
      box: $('#box').val(),
      isbn: $('#isbn').val(),
      title: title,
      creator: $('#creator').val(),
      publisher: $('#publisher').val(),
    };

    $.ajax({
      url: '/api/packing/v1/',
      method: 'POST',
      timeout: 10000,
      contentType: 'application/json',
      dataType: 'json',
      data: JSON.stringify(params),
    }).then(
      () => {
        this.removeSpinner('register')
        this.clearFields();
        this.loadDataTables();
        this.setFocusToKey();
      },
      () => {
        this.removeSpinner('register')
      }
    );
  }

  clearFields() {
    $('#isbn').val('');
    $('#title').val('');
    $('#creator').val('');
    $('#publisher').val('');
  }

  loadDataTables() {
    this.dataTable = $('#books').DataTable({
      autoWidth: false,
      serverSide: true,
      processing: true,
      responsive: true,
      // 再描画するので、destroy: trueにしておく
      // https://datatables.net/manual/tech-notes/3
      destroy: true,
      ajax: {
        url: '/datatables/books/',
        type: 'GET',
        data: {box: $('#box').val()},
      },
      columnDefs: [
        {targets: 0, data: 'id'},
        {targets: 1, data: 'ndl__isbn'},
        {targets: 2, data: 'title'},
        {targets: 3, data: 'creator'},
        {targets: 4, data: 'publisher'},
      ],
      // 登録順に表示したい
      order: [[0, 'desc']],
      // 最大表示したい
      pageLength: 100,
    });
  }

  setSpinner(btnId) {
    const btn = $(`#${btnId}`);
    btn.prop('disabled', true);
    btn.append(`<span id="${btnId}-spinner" class="spinner-border spinner-border-sm"></span>`)
  }

  removeSpinner(btnId) {
    $(`#${btnId}`).prop('disabled', false);
    $(`#${btnId}-spinner`).remove();
  }

  setFocusToKey() {
    $('#key').focus();
  }
}
