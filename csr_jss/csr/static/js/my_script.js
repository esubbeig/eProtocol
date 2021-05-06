
$(document).ready(function(){

  CKEDITOR.config.extraPlugins='colorbutton';
  CKEDITOR.config.extraPlugins = 'tableresize';
  CKEDITOR.config.extraPlugins = 'onchange';

  $('.accordion__header').click(function(e) {
  e.preventDefault();

  var currentIsActive = $(this).hasClass('is-active');
  $(this).parent('.accordion').find('> *').removeClass('is-active');

  if(currentIsActive != 1) {
    $(this).addClass('is-active');
    $(this).next('.accordion__body').addClass('is-active');


    var dynid = $(this).attr("data-id");

    $.ajax({

          url : $(this).attr("data-url"),
          type : 'GET',
          dataType : 'json',
          success : function(data){

            $("#p-" + dynid).html(data.html_form);

            CKEDITOR.replace('id_sec_content-'+dynid);
          }

        });
    }
  });


  $(document).on('submit', '.template_section_form', function(event){

    event.preventDefault();
    
    var form = $(this);
    $.ajax({
      url : form.attr('data-href'),
      method: form.attr('method'),
      data : form.serialize(),
      dataType : 'json',
      success: function(data){
        location.reload();
      }

    });
  });


  $("input[type='checkbox']").change(function() {
    if(this.checked) {
        $.ajax({

        url   : '/get_all_active_users_details',
        type  : "get",
        dataType : "json",
       
        success   : function(data){

          $('.admin_users_div').html(data.html_form);

          $('#admin_users').DataTable({

            searching : true,
            "ordering": true,
            columnDefs: [{
              orderable: false,
              targets: "no-sort"
            }]

          });
        
        }
    });      
    }
    else{

      $.ajax({

        url   : '/get_all_act_inact_users_details',
        type  : "get",
        dataType : "json",
       
        success   : function(data){

          $('.admin_users_div').html(data.html_form);

          $('#admin_users').DataTable({

            searching : true,
            "ordering": true,
            columnDefs: [{
              orderable: false,
              targets: "no-sort"
            }]

          });
        
        }
    });    
    }
  });

  $(document).on('shown.bs.modal', '#create_project_modal', function () {
  $('.chosen', this).chosen('destroy').chosen();
  });

  $(document).on('shown.bs.modal', '#modal-update-project', function () {
  $('.chosen', this).chosen('destroy').chosen();
  });

  $(document).on('shown.bs.modal', '#create_eprotocol_modal', function () {
  $('.chosen', this).chosen('destroy').chosen();
  });
  

  $('#audit_logs').DataTable({

    searching : false,
    "ordering": true,
    columnDefs: [{
      orderable: false,
      targets: "no-sort"
    }]

  });
  $('#activity_log').DataTable({

    searching : false,
    "ordering": true,
    columnDefs: [{
      orderable: false,
      targets: "no-sort"
    }]

  });
  $('#email_logs').DataTable({

    searching : true,
    "ordering": true,
    columnDefs: [{
      orderable: false,
      targets: "no-sort"
    }]

  });
  $('#admin_users').DataTable({

    searching : true,
    "ordering": true,
    columnDefs: [{
      orderable: false,
      targets: "no-sort"
    }]

  });

  $('#csr_projects_tbl').DataTable({

    searching : true,
    "ordering": true,
    columnDefs: [{
      orderable: false,
      targets: "no-sort"
    }]

  });

  $('#eprotocol_projects_tbl').DataTable({

    searching : true,
    "ordering": true,
    columnDefs: [{
      orderable: false,
      targets: "no-sort"
    }]

  });

  $('#eprotocol_templates_tbl').DataTable({

    searching : true,
    "ordering": true,
    columnDefs: [{
      orderable: false,
      targets: "no-sort"
    }]

  });

  $('#user_projects_tbl').DataTable({

    searching : true,
    "ordering": true,
    columnDefs: [{
      orderable: false,
      targets: "no-sort"
    }]

  });

  // to handle popping messages
  $('#error-message').delay(6000).fadeOut();

  // to get the file name in upload field
  $(document).on('change', 'input[type=file]', function(event){

    $('#dispaly_f_name').html(event.target.files[0].name);

  });

  $(document).on('click', '#disabled-edit-custome-csr-btn', function(){
      alert("You need to upload Custom CSR to edit mapping!");
  });

  $(document).on('click', '#disabled-map-csr-admin-btn', function(){
      alert("Please upload CSR, Protocol & SAR.");
  });

  $(document).on('click', '#user_create_form_disabled', function(){
      alert("Sorry! Email Configurations Not Set!");
  });

  // To create eProtocol Template
  $('#create_prot_temp_btn').click(function(){

    $.ajax({

        url   : $(this).attr('data-href'),
        type  : "get",
        dataType : "json",
        beforeSend : function(){

          $('#create_prot_temp_modal').modal({show : true, backdrop : 'static', keyboard : false});

        },
        success   : function(data){

          $('#create_prot_temp_modal .modal-content').html(data.html_form);
        }
    });      
  });

    $('#create_prot_temp_modal').on('submit', '.create_prot_temp_form', function(){

      $('#ajax_loader').show();

      var form = $(this);
      var formData = new FormData(this);

      $.ajax({

          url : form.attr('data-url'),
          data : formData,
          type : form.attr('method'),
          cache: false,
          processData: false,
          contentType: false,
          success : function(data){

              $('#ajax_loader').hide();

              if(data.form_is_valid){

                  $('#create_prot_temp_modal').modal('hide');
                  location.reload();

              }else{
                 $('#create_prot_temp_modal .modal-content').html(data.html_form);
              }
          }
      });
      return false;
  });
  

  // loads signup form into the user create modal
  $('#user_create_form').click(function(){

    $.ajax({

        url   : $(this).attr('data-href'),
        type  : "get",
        dataType : "json",
        beforeSend : function(){

          $('#create_user_modal').modal({show : true, backdrop : 'static', keyboard : false});

        },
        success   : function(data){

          $('#create_user_modal .modal-content').html(data.html_form);
        }
    });      
  });

  $('#create_user_modal').on('submit', '.create_user_form', function(){

      var form = $(this);
      $('#ajax_loader').show();
      
      $.ajax({

          url : form.attr('data-url'),
          data : form.serialize(),
          type : form.attr('method'),
          dataType : 'json',       
          success : function(data){

              $('#ajax_loader').hide();

              if(data.form_is_valid){

                  if(data.mail_status){
                    
                    $('#create_user_modal').modal('hide');
                    location.reload();
                  }else{

                    $('#create_user_modal').modal('hide');
                    location.reload();
                  }
                  

              }else{
                 $('#create_user_modal .modal-content').html(data.html_form);
              }
          }
          
      });
      return false;
  });

  // to handle create project form
  $('#project_create_form').click(function(){

    // $('#ajax_loader').show();

    $.ajax({

        url   : $(this).attr('data-href'),
        type  : "get",
        dataType : "json",
        beforeSend : function(){

          $('#create_project_modal').modal({show : true, backdrop : 'static', keyboard : false});
        },
        success   : function(data){

          $('#create_project_modal .modal-content').html(data.html_form);
          // $('#ajax_loader').hide();
        }
    });      
  });

  $('#create_project_modal').on('submit', '.create_project_form', function(){

      var form = $(this);

      $('#ajax_loader').show();

      $.ajax({

          url : form.attr('data-url'),
          data : form.serialize(),
          type : form.attr('method'),
          dataType : 'json',
          success : function(data){

              $('#ajax_loader').hide();

              if(data.form_is_valid){

                  $('#create_project_modal').modal('hide');
                  location.reload();

              }else{
                 $('#create_project_modal .modal-content').html(data.html_form);
                 $("select[name=therapeutic_area]").chosen('destroy').chosen();
              }
          }
      });
      return false;
  });

  // to handle project assigning
  $(document).on('click', '.project_assigning', function(){
    
    $.ajax({

        url : $(this).attr("data-href"),
        type  : "get",
        dataType : "json",
        beforeSend : function(){

          $('#assign_project_modal').modal({show : true, backdrop : 'static', keyboard : false});
          
        },

        success   : function(data){

          $('#assign_project_modal .modal-content').html(data.html_form);
          
        }
    });      
  });

  $('.assign_project_modal').on('submit', '.assign_project_form', function(){

      var form = $(this);

      $('#ajax_loader').show();

      $.ajax({

          url : form.attr('data-url'),
          data : form.serialize(),
          type : form.attr('method'),
          dataType : 'json',
          success : function(data){

              $('#ajax_loader').hide();

              if(data.form_is_valid){

                  $('.assign_project_modal').modal('hide');
                  location.reload();

              }else{

                 $('.assign_project_modal .modal-content').html(data.html_form);
                 $('.assign_project_modal .assin_at_least').show();

              }
          }
      });
      return false;
  });

  // to handle edit project
  $('#id_user_projects').on('click', '.update-project', function(){

        var btn = $(this);
        
        $.ajax({

            url : btn.attr('data-url'),
            type : 'get',
            dataType : 'json',
            beforeSend : function() {
              $('#modal-update-project').modal({show : true, backdrop : 'static', keyboard : false});
            },
            success : function(data) {
              $('#modal-update-project .modal-content').html(data.html_form);
            }


        });
  });

  $('#modal-update-project').on('submit', '.edit_project_form', function() {

    var form = $(this);

    $('#ajax_loader').show();

    $.ajax({
      url : form.attr('data-url'),
      data : form.serialize(),
      type : form.attr('method'),
      dataType : 'json',
      success : function(data){

          $('#ajax_loader').hide();

          if(data.form_is_valid) {

              $('#modal-update-project').modal('hide');
              location.reload();
          }
          else {
            $('#modal-update-project .modal-content').html(data.html_form);
             $("select[name=therapeutic_area]").chosen('destroy').chosen();
          }
      }
    });
    return false;
  });

  // to handle search user projects
  $('#id_search_user_project').on('keyup keypress', function(e) {

    var keyCode = e.keyCode || e.which;
    
    if (keyCode === 13) {
        e.preventDefault();
        return false;
    }
    $.ajax({

        type : 'GET',
        url  : $(this).attr('name'),
        data : {
          'search_user_project' : $('#id_search_user_project').val(),
          'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val(),
        },
        dataType : 'html',
        success : function(data) {
          $('#id_user_projects').html(data);
        },

    });

  });

    // to handle search admin projects
  $('#id_search_admin_project').on('keyup keypress', function(e) {

    // $('.clear__btn').show();

    var keyCode = e.keyCode || e.which;
    
    if (keyCode === 13) {
        e.preventDefault();
        return false;
    }
    $.ajax({

        url  : $(this).attr('name'),
        type : 'GET',
        data : {
          'search_admin_project' : $('#id_search_admin_project').val(),
          'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val(),
        },
        dataType : 'html',
        success : function(data) {
          $('#id_admin_projects').html(data);
        },

    });

  });

  $(document).on('click', '.clear__btn', function(){

    $('#id_search_admin_project').val('');
    $(this).hide();

  });

  // to handle change password
  $('#change_password_link').click(function(){

    // $('#ajax_loader').show();
    $('.submenu').hide();
    
    $.ajax({

        url   : $(this).attr('data-href'),
        type  : "get",
        dataType : "json",
        beforeSend : function(){

          $('#change_password_modal').modal({show : true, backdrop : 'static', keyboard : false});
        },
        success   : function(data){

          $('#change_password_modal .modal-content').html(data.html_form);

          // $('#ajax_loader').hide();
        }
    });      
  });

  $('#change_password_modal').on('submit', '.change_password_form', function(){

      var form = $(this);
      // $('#spin_loader').show();

      $.ajax({

          url : form.attr('data-url'),
          data : form.serialize(),
          type : form.attr('method'),
          dataType : 'json',
          success : function(data){

              // $('#spin_loader').hide();

              if(data.form_is_valid){

                  $('#change_password_modal').modal('hide');
                  location.reload();

              }else{
                 $('#change_password_modal .modal-content').html(data.html_form);
              }
          }
      });
      return false;
  });

  // To handle csr admin upload
  $('#upload_csr_admin_form').click(function(){


    var is_Exist = $('#csr_doc_exist_or_not').val();

    if(is_Exist == '1'){

      var r = confirm("Uploading new Template will erase already mapped Configurations! Click on OK to continue.")
      if (r == true){
      
        $.ajax({

            url   : $(this).attr('data-href'),
            type  : "get",
            dataType : "json",
            beforeSend : function(){

              $('#upload_csr_admin_modal').modal({show : true, backdrop : 'static', keyboard : false});
            },
            success   : function(data){

              $('#upload_csr_admin_modal .modal-content').html(data.html_form);
          
            }
        });
        }else{
          return false;
        }

    }else{

      $.ajax({

            url   : $(this).attr('data-href'),
            type  : "get",
            dataType : "json",
            beforeSend : function(){

              $('#upload_csr_admin_modal').modal({show : true, backdrop : 'static', keyboard : false});
            },
            success   : function(data){

              $('#upload_csr_admin_modal .modal-content').html(data.html_form);
          
            }
        });

    }

        
  });

  $('#upload_csr_admin_modal').on('submit', '.admin_upload_csr_form', function(){

      $('#ajax_loader').show();

      var form = $(this);
      var formData = new FormData(this);

      $.ajax({

          url : form.attr('data-url'),
          data : formData,
          type : form.attr('method'),
          cache: false,
          processData: false,
          contentType: false,
          success : function(data){

              $('#ajax_loader').hide();

              if(data.form_is_valid){

                  $('#upload_csr_admin_modal').modal('hide');
                  location.reload();

              }else{
                 $('#upload_csr_admin_modal .modal-content').html(data.html_form);
                 if (data.file_data_format != ''){
                    $('#upload_csr_admin_modal .modal-content #error_format').html('Document contains wrong formating at section "'+data.file_data_format+'"');
                 }
              }
          }
      });
      return false;
  });
  // To handle admin protocol upload
  $('#upload_protocol_admin_form').click(function(){

    var is_Exist = $('#protocol_doc_exist_or_not').val();

    if(is_Exist == '1'){

      var r = confirm("Uploading new Protocol will effect already mapped Configurations! Click on OK to continue.")
      if (r == true){
    
        $.ajax({

            url   : $(this).attr('data-href'),
            type  : "get",
            dataType : "json",
            beforeSend : function(){

              $('#upload_protocol_admin_modal').modal({show : true, backdrop : 'static', keyboard : false});
            },
            success   : function(data){

              $('#upload_protocol_admin_modal .modal-content').html(data.html_form);
              // $('#ajax_loader').hide();
            }
        });
      }else{
        return false;
      }
    }else{
      $.ajax({

            url   : $(this).attr('data-href'),
            type  : "get",
            dataType : "json",
            beforeSend : function(){

              $('#upload_protocol_admin_modal').modal({show : true, backdrop : 'static', keyboard : false});
            },
            success   : function(data){

              $('#upload_protocol_admin_modal .modal-content').html(data.html_form);
              // $('#ajax_loader').hide();
            }
        });
    }

  });

  $('#upload_protocol_admin_modal').on('submit', '.admin_upload_protocol_form', function(){

      $('#ajax_loader').show();

      var form = $(this);
      var formData = new FormData(this);

      $.ajax({

          url : form.attr('data-url'),
          data : formData,
          type : form.attr('method'),
          cache: false,
          processData: false,
          contentType: false,
          success : function(data){

              $('#ajax_loader').hide();

              if(data.form_is_valid){

                  $('#upload_protocol_admin_modal').modal('hide');
                  location.reload();

              }else{
                 $('#upload_protocol_admin_modal .modal-content').html(data.html_form);
                 if (data.file_data_format != ''){
                    $('#upload_protocol_admin_modal .modal-content #error_format').html('Document contains wrong formating at section "'+data.file_data_format+'"');
                 }
              }
          }
      });
      return false;
  });

  // To handle admin sar upload
  $('#upload_sar_admin_form').click(function(){

    var is_Exist = $('#sar_doc_exist_or_not').val();

    if(is_Exist == '1'){

      var r = confirm("Uploading new SAR will effect already mapped Configurations! Click on OK to continue.")
      if (r == true){
    
        $.ajax({

            url   : $(this).attr('data-href'),
            type  : "get",
            dataType : "json",
            beforeSend : function(){

              $('#upload_sar_admin_modal').modal({show : true, backdrop : 'static', keyboard : false});
            },
            success   : function(data){

              $('#upload_sar_admin_modal .modal-content').html(data.html_form);

              // $('#ajax_loader').hide();
            }
        });
      }else{
        return false;
      }
    }else{
      $.ajax({

        url   : $(this).attr('data-href'),
        type  : "get",
        dataType : "json",
        beforeSend : function(){

          $('#upload_sar_admin_modal').modal({show : true, backdrop : 'static', keyboard : false});
        },
        success   : function(data){

          $('#upload_sar_admin_modal .modal-content').html(data.html_form);

          // $('#ajax_loader').hide();
        }
    });
    }
          
  });

  $('#upload_sar_admin_modal').on('submit', '.admin_upload_sar_form', function(){

      $('#ajax_loader').show();

      var form = $(this);
      var formData = new FormData(this);

      $.ajax({

          url : form.attr('data-url'),
          data : formData,
          type : form.attr('method'),
          cache: false,
          processData: false,
          contentType: false,
          success : function(data){

              $('#ajax_loader').hide();

              if(data.form_is_valid){

                  $('#upload_sar_admin_modal').modal('hide');
                  location.reload();

              }else{
                 $('#upload_sar_admin_modal .modal-content').html(data.html_form);
              }
          }
      });
      return false;
  });

  // to change the copy headings by changing source in admin csr mapping
  $(document).on('change', '.source_file_select',  function(){

      var a = $(this).attr('data-target');
      var v = $(this).val();
      var protocol_headings_list = JSON.parse($('#protocol_headings_list').val());   
      var sar_headings_list      = JSON.parse($('#sar_headings_list').val());

      var opt_html = '<option value="">---------</option>';
      
      if(v == 'Protocol')
      {
        $.each(protocol_headings_list, function(key,value){

          opt_html += "<option value='"+ value +"'>"+ value +"</option>";

        });

        $(a).html(opt_html);
      }
      else if(v == 'SAR')
      {
        $.each(sar_headings_list, function(key,value){

          opt_html += "<option value='"+ value +"'>"+ value +"</option>";

        });

        $(a).html(opt_html);
      }
      else
      {
        $(a).html('<option value="">---------</option>');
      }
  });

  // to add record in admin csr mapping
  $(document).on('click', '.add_record', function(){

    var no_of_records = $('#records_length').val();

    var proto_head = parseInt($('#protocol_headings_length').val());

    var sar_head = parseInt($('#sar_headings_length').val());

    // alert(no_of_records);

    var no_of_records_update = parseInt(no_of_records) + 1;

    var a = $(this).attr('data-target');

    var b = $(a).find('.csr_heading').val();

    // var c = $(a).find('.parent_id').val();

    var src = $(a).find('.source_file_select').val();

    var src_hd = $(a).find('.source_file_headings').val();

    if(src != '' && src_hd != ''){

        $('#ajax_loader').show();

        html = '';

        html += '<tr class="no-brd" id="record-'+ no_of_records_update +'">';

        html += '<td><input type="hidden" class="child_parent_id" name="child_parent_id[]" value="' + b + '"><input class="form-control csr_heading" hidden type="text" readonly value="'+ b +'" id="csr-heading-'+ no_of_records_update +'" name="csr_headings[]"></td>'

        html += '<td><select class="form-control source_file_select" required data-target="#copy-heading-'+ no_of_records_update +'" name="source[]" id="source-'+ no_of_records_update +'"><option value="">Source</option>';

        if(proto_head > 0 && sar_head > 0){

          html += '<option value="Protocol">Protocol</option><option value="SAR">SAR</option>';

        }else{

          if(proto_head > 0){

            html += '<option value="Protocol">Protocol</option>';

          }else if(sar_head > 0){

            html += '<option value="SAR">SAR</option>';
          }
        }

        html += '</select></td>';

        html += '<td><select class="form-control source_file_headings" required id="copy-heading-'+ no_of_records_update +'" name="copy_headings[]"><option value="">------</option></select></td>';

        html += '<td><input type="button" class="remove_record" value="" ></td></tr>';

        $(html).insertAfter($(this).closest('tr'));

        $('#records_length').val(no_of_records_update);

        $('#ajax_loader').hide();

    }
    else{
      alert('Please Map '+ b +' to add more ...');
    }

  });

  // to add record in admin csr mapping if already pre mapped
  $(document).on('click', '.add_record_prem', function(){
       
    var no_of_records = $('#records_length').val();

    var proto_head = parseInt($('#protocol_headings_length').val());

    var sar_head = parseInt($('#sar_headings_length').val());

    var no_of_records_update = parseInt(no_of_records) + 1;

    var a = $(this).attr('data-target');

    var b = $(a).find('.csr_heading').val();

    var c = $(a).find('.parent_id').val();

    var src = $(a).find('.source_file_select').val();

    var src_hd = $(a).find('.source_file_headings').val();

    if(src != '' && src_hd != ''){

      $('#ajax_loader').show();

      $.ajax({
          url : "ad_csr_headings",
          type : "get",
          dataType : "json",
          success : function(data){

            html = '';

            // html += '<tr id="record">';

            html += '<tr class="no-brd" id="record-'+ no_of_records_update +'">';

            // html += data.html_form;
            html += '<td><input type="hidden" class="child_parent_id" name="child_parent_id[]" value="' + c + '"><input class="form-control csr_heading" hidden type="text" readonly value="'+ b +'" id="csr-heading-'+ no_of_records_update +'" name="csr_headings[]"></td>';

            // html += '</select></td>'

            // html += '<td><select class="form-control source_file_select" data-target="#copy-heading-'+ no_of_records_update +'" name="source[]" id="source-'+ no_of_records_update +'"><option value="">Source</option>';
            html += '<td><select class="form-control source_file_select" required data-target="#copy-heading-'+ no_of_records_update +'" name="source[]" id="source-'+ no_of_records_update +'"><option value="">Source</option>';

            if(proto_head > 0 && sar_head > 0){

              html += '<option value="Protocol">Protocol</option><option value="SAR">SAR</option>';
        
            }else{

              if(proto_head > 0){

                html += '<option value="Protocol">Protocol</option>';

              }else if(sar_head > 0){

                html += '<option value="SAR">SAR</option>';
              }
            }

            html += '</select></td>';

            html += '<td><select class="form-control source_file_headings" required id="copy-heading-'+ no_of_records_update +'" name="copy_headings[]"><option value="">------</option></select></td>';

            html += '<td><input type="button" class="remove_record" value="" ></td></tr>';

            $(html).insertAfter(a);
            // $(html).insertAfter($(this).closest('tr'));

            $('#records_length').val(no_of_records_update);

            $('#ajax_loader').hide();
          }
      });
    }
    else{
      alert('Please Map '+ b +' to add more ...');
    }

  });

  // to remove record in admin csr mapping
  $(document).on('click', '.remove_record', function(){

    var no_of_records = $('#records_length').val();

    // alert(no_of_records);

    var no_of_records_update = parseInt(no_of_records) - 1;

    $(this).closest('tr').remove();

    $('#records_length').val(no_of_records_update);

  });

  // To handle csr user upload
  $('#upload_csr_form').click(function(){

    var is_Exist = $('#custom_csr_doc_exist_or_not').val();

    if(is_Exist == '1'){

      var r = confirm("Uploading new Template will erase already mapped Configurations! Click on OK to continue.")
      if (r == true){
    
        $.ajax({

            url   : $(this).attr('data-href'),
            type  : "get",
            dataType : "json",
            beforeSend : function(){

              $('#upload_csr_modal').modal({show : true, backdrop : 'static', keyboard : false});
            },
            success   : function(data){

              $('#upload_csr_modal .modal-content').html(data.html_form);
              // $('#ajax_loader').hide();
            }
        });
      }else{
        return false;
      }
    }else{
      $.ajax({

        url   : $(this).attr('data-href'),
        type  : "get",
        dataType : "json",
        beforeSend : function(){

          $('#upload_csr_modal').modal({show : true, backdrop : 'static', keyboard : false});
        },
        success   : function(data){

          $('#upload_csr_modal .modal-content').html(data.html_form);
          // $('#ajax_loader').hide();
        }
    });
    }     
  });

  $('#upload_csr_modal').on('submit', '.upload_csr_form', function(){

      $('#ajax_loader').show();

      var form = $(this);
      var formData = new FormData(this);

      $.ajax({

          url : form.attr('data-url'),
          data : formData,
          type : form.attr('method'),
          cache: false,
          processData: false,
          contentType: false,
          success : function(data){

              $('#ajax_loader').hide();

              if(data.form_is_valid){

                  // alert('File uploaded succesfully');
                  $('#upload_csr_modal').modal('hide');
                  location.reload();

              }else{
                 $('#upload_csr_modal .modal-content').html(data.html_form);
                 if (data.file_data_format != ''){
                    $('#upload_csr_modal .modal-content #error_format').html('Document contains wrong formating at section "'+data.file_data_format+'"');
                 }
              }
          }
      });
      return false;
  });

   // To handle user protocol upload
  $('#upload_protocol_form').click(function(){
    
    var is_Exist = $('#usr_protocol_doc_exist_or_not').val();

    if(is_Exist == '1'){

      var r = confirm("Uploading new Protocol will effect already mapped Configurations! Click on OK to continue.")
      if (r == true){

        $.ajax({

            url   : $(this).attr('data-href'),
            type  : "get",
            dataType : "json",
            beforeSend : function(){

              $('#upload_protocol_modal').modal({show : true, backdrop : 'static', keyboard : false});
            },
            success   : function(data){

              $('#upload_protocol_modal .modal-content').html(data.html_form);
              // $('#ajax_loader').hide();
            }
        });
      }else{
        return false;
      }
    }else{
      $.ajax({

        url   : $(this).attr('data-href'),
        type  : "get",
        dataType : "json",
        beforeSend : function(){

          $('#upload_protocol_modal').modal({show : true, backdrop : 'static', keyboard : false});
        },
        success   : function(data){

          $('#upload_protocol_modal .modal-content').html(data.html_form);
          // $('#ajax_loader').hide();
        }
    });
    }   
  });

  $('#upload_protocol_modal').on('submit', '.upload_protocol_form', function(){

      $('#ajax_loader').show();

      var form = $(this);
      var formData = new FormData(this);

      $.ajax({

          url : form.attr('data-url'),
          data : formData,
          type : form.attr('method'),
          cache: false,
          processData: false,
          contentType: false,
          success : function(data){

              $('#ajax_loader').hide();

              if(data.form_is_valid){

                  // alert('File uploaded succesfully');
                  $('#upload_protocol_modal').modal('hide');
                  location.reload();

              }else{
                 $('#upload_protocol_modal .modal-content').html(data.html_form);
                 if (data.file_data_format != ''){
                    $('#upload_protocol_modal .modal-content #error_format').html('Document contains wrong formating at section "'+data.file_data_format+'"');
                 }
              }
          }
      });
      return false;
  });

  // To handle user sar upload
  $('#upload_sar_form').click(function(){

    var is_Exist = $('#usr_sar_doc_exist_or_not').val();

    if(is_Exist == '1'){

      var r = confirm("Uploading new SAR will effect already mapped Configurations! Click on OK to continue.")
      if (r == true){
    
        $.ajax({

            url   : $(this).attr('data-href'),
            type  : "get",
            dataType : "json",
            beforeSend : function(){

              $('#upload_sar_modal').modal({show : true, backdrop : 'static', keyboard : false});
            },
            success   : function(data){

              $('#upload_sar_modal .modal-content').html(data.html_form);
              // $('#ajax_loader').hide();
            }
        });
      }else{
        return false;
      }
    }else{
      $.ajax({

        url   : $(this).attr('data-href'),
        type  : "get",
        dataType : "json",
        beforeSend : function(){

          $('#upload_sar_modal').modal({show : true, backdrop : 'static', keyboard : false});
        },
        success   : function(data){

          $('#upload_sar_modal .modal-content').html(data.html_form);
          // $('#ajax_loader').hide();
        }
    });
    }    
  });

  $('#upload_sar_modal').on('submit', '.upload_sar_form', function(){

      $('#ajax_loader').show();

      var form = $(this);
      var formData = new FormData(this);

      $.ajax({

          url : form.attr('data-url'),
          data : formData,
          type : form.attr('method'),
          cache : false,
          processData: false,
          contentType: false,
          success : function(data){

              $('#ajax_loader').hide();

              if(data.form_is_valid){

                  // alert('File uploaded succesfully');
                  $('#upload_sar_modal').modal('hide');
                  location.reload();

              }else{
                 $('#upload_sar_modal .modal-content').html(data.html_form);
              }
          }
      });
      return false;
  });

  // to change the copy headings by changing source in user csr mapping
  $(document).on('change', '.source_file_select_usr',  function(){
      
      
      var proj_id = $('#project_id').val();
              
      var a = $(this).attr('data-target');
      var v = $(this).val();

      var protocol_headings_list = JSON.parse($('#usr_protocol_headings_list').val());   
      var sar_headings_list      = JSON.parse($('#usr_sar_headings_list').val());

      var opt_html = '<option value="">---------</option>';

      
      if(v == 'Protocol')
      {

       $.each(protocol_headings_list, function(key,value){

          opt_html += "<option value='"+ value +"'>"+ value +"</option>";

        });

        $(a).html(opt_html);

      }
      else if(v == 'SAR')
      {
        
        $.each(sar_headings_list, function(key,value){

          opt_html += "<option value='"+ value +"'>"+ value +"</option>";

        });

        $(a).html(opt_html);

      }
      else
      {
        $(a).html('<option value="">---------</option>');
      }
  });

  // to add record in user csr mapping
  $(document).on('click', '.add_record_user', function(){

    var no_of_records = $('#records_length').val();

    var proto_head = parseInt($('#protocol_headings_length').val());

    var sar_head = parseInt($('#sar_headings_length').val());

    var no_of_records_update = parseInt(no_of_records) + 1;

    var a = $(this).attr('data-target');

    var b = $(a).find('.csr_heading_usr').val();

    var src = $(a).find('.source_file_select_usr').val();

    var src_hd = $(a).find('.source_file_headings_usr').val();

    if(src != '' && src_hd != ''){

        $('#ajax_loader').show();

        html = '';

        html += '<tr class="no-brd" id="record-'+ no_of_records_update +'">';

        html += '<td><input type="hidden" class="child_parent_id" name="child_parent_id[]" value="' + b + '"><input class="form-control csr_heading_usr" hidden type="text" readonly value="'+ b +'" id="csr-heading-usr-'+ no_of_records_update +'" name="csr_headings[]"></td>'

        html += '<td><select class="form-control source_file_select_usr" data-target="#copy-heading-usr-'+ no_of_records_update +'" name="source[]" id="source-usr-'+ no_of_records_update +'"><option value="">Source</option>';

        if(proto_head > 0 && sar_head > 0){

          html += '<option value="Protocol">Protocol</option><option value="SAR">SAR</option>';

        }else{

          if(proto_head > 0){

            html += '<option value="Protocol">Protocol</option>';

          }else if(sar_head > 0){

            html += '<option value="SAR">SAR</option>';
          }
        }

        html += '</select></td>';

        html += '<td><select class="form-control source_file_headings_usr" id="copy-heading-usr-'+ no_of_records_update +'" name="copy_headings[]"><option value="">------</option></select></td>';

        html += '<td><input type="button" class="remove_record_user" value="" ></td></tr>';

        $(html).insertAfter($(this).closest('tr'));

        $('#records_length').val(no_of_records_update);

        $('#ajax_loader').hide();
    }
    else{
      alert('Please Map '+ b +' to add more ...');
    }

  });

  // to add record in user csr mapping if already pre mapped
  $(document).on('click', '.add_record_usr_prem', function(){

    var proj_id = $('#project_id').val();

    var proto_head = parseInt($('#protocol_headings_length').val());

    var sar_head = parseInt($('#sar_headings_length').val());
       
    var no_of_records = $('#records_length').val();

    var no_of_records_update = parseInt(no_of_records) + 1;

    var a = $(this).attr('data-target');

    var b = $(a).find('.csr_heading_usr').val();

    var c = $(a).find('.parent_id').val();

    var src = $(a).find('.source_file_select_usr').val();

    var src_hd = $(a).find('.source_file_headings_usr').val();

    if(src != '' && src_hd != ''){

        $('#ajax_loader').show();

        $.ajax({
            url : "/usr_csr_headings/" + proj_id,
            type : "get",
            dataType : "json",
            success : function(data){

              html = '';

              html += '<tr class="no-brd" id="record-'+ no_of_records_update +'">';

              // html += '<td><select class="form-control csr_heading_usr" name="csr_headings[]">';

              // html += data.html_form;
              html += '<td><input type="hidden" class="child_parent_id" name="child_parent_id[]" value="' + c + '"><input class="form-control csr_heading_usr" hidden type="text" readonly value="'+ b +'" id="csr-heading-usr-'+ no_of_records_update +'" name="csr_headings[]"></td>';

              // html += '</select></td>'

              html += '<td><select class="form-control source_file_select_usr" data-target="#copy-heading-usr-'+ no_of_records_update +'" name="source[]" id="source-'+ no_of_records_update +'"><option value="">Source</option>';

              if(proto_head > 0 && sar_head > 0){

                html += '<option value="Protocol">Protocol</option><option value="SAR">SAR</option>';
          
              }else{

                if(proto_head > 0){

                  html += '<option value="Protocol">Protocol</option>';

                }else if(sar_head > 0){

                  html += '<option value="SAR">SAR</option>';
                }
              }

              html += '</select></td>';

              html += '<td><select class="form-control source_file_headings_usr" id="copy-heading-usr-'+ no_of_records_update +'" name="copy_headings[]"><option value="">------</option></select></td>';

              html += '<td><input type="button" class="remove_record_user" value="" ></td></tr>';

              $(html).insertAfter(a);

              $('#records_length').val(no_of_records_update);

              $('#ajax_loader').hide();
            }
        });
    }
    else{
      alert('Please Map '+ b +' to add more ...');
    }

  });

  // to remove record in user csr mapping
  $(document).on('click', '.remove_record_user', function(){

    var no_of_records = $('#records_length').val();

    // alert(no_of_records);

    var no_of_records_update = parseInt(no_of_records) - 1;

    $(this).closest('tr').remove();

    $('#records_length').val(no_of_records_update);

  });

  // To handle onchange event for activity log events in admin
  $(document).on('change', '#activity_log_on_change', function(){

    $('#ajax_loader').show();

    var url = $(this).val();
    
    $.ajax({
      url : url,
      type : "get",
      dataType : "json",
      success : function(data){

        $('#ajax_loader').hide();

        $('#activity_log_data').html(data.html_form);
        $('#activity_log_bread').html(data.username);
        $('#activity_log').DataTable({

          searching : false,
          "ordering": true,
          columnDefs: [{
            orderable: false,
            targets: "no-sort"
          }]

        });
      }
    });

  });

  // To handle onchange event for audit log events in admin
  $(document).on('change', '#audit_log_on_change', function(){

    $('#ajax_loader').show();

    var url = $(this).val();
    
    $.ajax({
      url : url,
      type : "get",
      dataType : "json",
      success : function(data){

        $('#ajax_loader').hide();

        $('#audit_log_data').html(data.html_form);
        $('#audit_log_bread').html(data.username);
        $('#audit_logs').DataTable({

          searching : false,
          "ordering": true,
          columnDefs: [{
            orderable: false,
            targets: "no-sort"
          }]

        });
      }
    });

  });

  // to show the confirmatin and take reason input form the user in user csr mapping
  $(document).on('click', '#edit_mapping_user_btn', function(e){

    // $('#ajax_loader').show();
    
    var url = $('#edit_mapping_user_form').attr('data-url');

    var csr_headings = $(".csr_heading_usr").map(function(){return $(this).val();}).get();
    var source = $(".source_file_select_usr").map(function(){return $(this).val();}).get();
    var source_headings = $(".source_file_headings_usr").map(function(){return $(this).val();}).get();
    var parent_ids = $(".child_parent_id").map(function(){return $(this).val();}).get();
    
    var values = [csr_headings, source, source_headings, parent_ids];
    var jsonText = JSON.stringify(values);

    $.ajax({
            // url : "/confirm_csr_mapping_user/",
            url : url,
            type : "post",
            data : jsonText,
            dataType : "json",
            success : function(data){

              // $('#ajax_loader').hide();

              $('#confirm_user_mapping_modal .modal-content').html(data.html_form);

              $('.confirm_map_user').on('click', function(){

                var k = $('#id_reason').val();
                
                if($.trim(k).length === 0)
                {

                    $('#error_reason').html("reason can't be blank");

                }else{

                    $('#confirm_user_mapping_modal').modal('hide');
                    $('#edit_mapping_user_form').submit();
                }

              });
            }
          });
  });

  // to show the confirmatin and take reason input form the admin in admin csr mapping
  $(document).on('click', '#edit_mapping_admin_btn', function(e){

    // $('#ajax_loader').show();

    var url = $('#admin-csr-mapping-form').attr('data-url');

    var csr_headings = $(".csr_heading").map(function(){return $(this).val();}).get();
    var source = $(".source_file_select").map(function(){return $(this).val();}).get();
    var source_headings = $(".source_file_headings").map(function(){return $(this).val();}).get();
    var parent_ids = $(".child_parent_id").map(function(){return $(this).val();}).get();
    
    var values = [csr_headings, source, source_headings, parent_ids];
    var jsonText = JSON.stringify(values);

    $.ajax({

      url : url,
      type : "post",
      data : jsonText,
      dataType : "json",
      success : function(data){

        // $('#ajax_loader').hide();

        $('#confirm_admin_mapping_modal .modal-content').html(data.html_form);
        $('.confirm_map_admin').on('click', function(){

          var k = $('#id_reason').val();
          
          if($.trim(k).length === 0)
          {

              $('#error_reason').html("reason can't be blank");

          }else{

              $('#confirm_admin_mapping_modal').modal('hide');
              $('#admin-csr-mapping-form').submit();
          }
      });

      }

    });    

  });


  // to show the confirmatin and take the file & version in generate csr
  $(document).on('click', '#generate_csr_link', function(e){

    var url = $(this).attr('data-href');
    
    $('.confirm_generate_csr').on('click', function(){

      var filename = $('#id_output_file_name').val();
      var version = $('input[name=version]:checked').val();

      var values = [filename, version];
      var jsonText = JSON.stringify(values);
      
      if($.trim(filename).length === 0)
      {

          $('#error_output_file_name').html("document name can't be blank");

      }else{

          $('#confirm_generate_csr_modal').modal('hide');
          $('#ajax_loader').show();

          $.ajax({
            url : url,
            type : "post",
            data : jsonText,
            dataType : "json",
            success : function(data){

              $('#ajax_loader').hide();

              if(data.form_is_valid){
              // alert('CSR generated succesfully!');
              location.reload();
            }
            else{
              // alert('Custom Mapping not found. Please map through Edit Mapping!');
              location.reload();
            }
            }
          });
      }
    });

  });

  // to handle email configuration
  $('#email_configuration_link').click(function(){

    $('#ajax_loader').show();
    
    $.ajax({

        url   : $(this).attr('data-href'),
        type  : "get",
        dataType : "json",
        beforeSend : function(){
          $('.submenu').hide();
          $('#email_configuration_modal').modal({show : true, backdrop : 'static', keyboard : false});
        },
        success   : function(data){

          $('#email_configuration_modal .modal-content').html(data.html_form);
          $('#ajax_loader').hide();
        }
    });      
  });

  $('#email_configuration_modal').on('submit', '.email_configuration_form', function(){

      $('#ajax_loader').show();

      var form = $(this);

      $.ajax({

          url : form.attr('data-url'),
          data : form.serialize(),
          type : form.attr('method'),
          dataType : 'json',
          success : function(data){

              $('#ajax_loader').hide();

              if(data.form_is_valid){

                  // alert('Email Configuration added succesfully');
                  $('#email_configuration_modal').modal('hide');
                  location.reload();

              }else{
                 $('#email_configuration_modal .modal-content').html(data.html_form);
              }
          }
      });
      return false;
  });

  // to handle resent email
  $(document).on('click', '#resend_email_button', function(){

    $('#ajax_loader').show();
  
    $.ajax({

        url   : $(this).attr('data-href'),
        type  : "get",
        dataType : "json",
        success   : function(data){

          $('#ajax_loader').hide();

          if(data.resend_status){
              // alert('Resend Email succesfully!');
              location.reload();
          }else{
              // alert('Problem with connecting SMTP server. Please check the Email Configurations!');
          }
        }
    });      
  });

  $(document).on('click', '#user_activate_link', function(){
    
    $.ajax({
      url : $(this).attr('data-href'),
      type : 'get',
      dataType: 'json',
      success : function(data){
        if(data.status){
          $('#user_act_status_modal').modal({show : true, backdrop : 'static', keyboard : false});
          $('#user_act_status_modal .modal-body').html('User activated successfully!');
        }else{
          $('#user_act_status_modal').modal({show : true, backdrop : 'static', keyboard : false});
          $('#user_act_status_modal .modal-body').html('Sorry! User not set the password yet.');
        }
      }
    });
  });

  $(document).on('click', '#user_deactivate_link', function(){
    
    $.ajax({
      url : $(this).attr('data-href'),
      type : 'get',
      dataType: 'json',
      success : function(data){
        if(data.status){
          $('#user_act_status_modal').modal({show : true, backdrop : 'static', keyboard : false});
          $('#user_act_status_modal .modal-body').html('User deactivated successfully!');
        }
      }
    });
  });

  $(document).on('click', '#user_act_status_modal_ok_btn', function(){
    location.reload();
  });


  // to handle create eprotocol form
  $('#eprotocol_create_form').click(function(){

    $.ajax({

        url   : $(this).attr('data-href'),
        type  : "get",
        dataType : "json",
        beforeSend : function(){

          $('#create_eprotocol_modal').modal({show : true, backdrop : 'static', keyboard : false});
        },
        success   : function(data){

          $('#create_eprotocol_modal .modal-content').html(data.html_form);
        }
    });      
  });

  $('#create_eprotocol_modal').on('submit', '.create_eprotocol_form', function(event){

    event.preventDefault();

    var form = $(this);

    $.ajax({

        url : form.attr('data-url'),
        data : form.serialize(),
        type : form.attr('method'),
        dataType : 'json',
        
        success   : function(data){

          if(data.form_is_valid){

            $('#create_eprotocol_modal').modal('hide');
            location.reload();

          }else{
            $('#create_eprotocol_modal .modal-content').html(data.html_form);
          }
        }
    });
    return false;      
  });

  // to handle clone eprotocol form
  $(document).on('click', '#clone_eprotocol_link', function(){

    $.ajax({

        url   : $(this).attr('data-href'),
        type  : "get",
        dataType : "json",
        beforeSend : function(){

          $('#clone_eprotocol_modal').modal({show : true, backdrop : 'static', keyboard : false});
        },
        success   : function(data){

          $('#clone_eprotocol_modal .modal-content').html(data.html_form);
        }
    });      
  });

  $('#clone_eprotocol_modal').on('submit', '.clone_eprotocol_form', function(event){

    event.preventDefault();

    var form = $(this);

    $.ajax({

        url : form.attr('data-url'),
        data : form.serialize(),
        type : form.attr('method'),
        dataType : 'json',
        
        success   : function(data){

          if(data.form_is_valid){

            $('#clone_eprotocol_modal').modal('hide');
            location.reload();

          }else{
            $('#clone_eprotocol_modal .modal-content').html(data.html_form);
          }
        }
    });      
  });


  $(document).on('click', '#import_prot_temp_data_link', function(){

    $.ajax({
      url : $(this).attr('data-href'),
      type: 'GET',
      dataType: 'json',
      beforeSend: function(){
        $('#import_prot_temp_data_modal').modal({show : true, backdrop : 'static', keyboard : false});
      },
      success : function(data){
        $('#import_prot_temp_data_modal .modal-content').html(data.html_form);
      }
    });

  });


  // To import content in eProtocol Template
  $('#import_prot_temp_data_modal').on('submit', '#import_template_content_form', function(){

    var formData = new FormData(this);

    $.ajax({

        url   : $(this).attr('data-href'),
        type  : "POST",
        dataType : "json",
        data : formData,
        cache: false,
        processData: false,
        contentType: false,
        success   : function(data){
          if(data.form_is_valid){
            
            $('#import_prot_temp_data_modal').modal('hide');
            location.reload();
          }else{
            
            $('#import_prot_temp_data_modal .modal-content').html(data.html_form);
          }
        }
    });      
  });

  $(document).on('click', '#archive_eprotocol_link', function(){

    $.ajax({
      url : $(this).attr('data-href'),
      type : 'get',
      dataType: 'json',
      beforeSend: function(){
        $('#archive_eprotocol_modal').modal({show : true, backdrop : 'static', keyboard : false});
      },
      success : function(data){
        $('#archive_eprotocol_modal .modal-content').html(data.html_form);
      }
    });
  });

  $('#archive_eprotocol_modal').on('submit', '#archive_eprotocol_form', function(){

    $.ajax({
      url : $(this).attr('data-href'),
      type : 'POST',
      dataType: 'json',
      success : function(data){
        
        $('#archive_eprotocol_modal').modal('hide');
        location.reload();
      }
    });
  });

  // $(document).on('click', '#unarchive_eprotocol_link', function(){

  //   $.ajax({
  //     url : $(this).attr('data-href'),
  //     type : 'get',
  //     dataType: 'json',
  //     success : function(data){
  //       if(data.status){
  //         location.reload();
  //       }
  //     }
  //   });
  // });


  $(document).on('click', '#delete_etemplate_link', function(){

    $.ajax({
      url : $(this).attr('data-href'),
      type : 'get',
      dataType: 'json',
      beforeSend: function(){
        $('#delete_etemplate_modal').modal({show : true, backdrop : 'static', keyboard : false});
      },
      success : function(data){
        $('#delete_etemplate_modal .modal-content').html(data.html_form);
      }
    });
  });

  $('#delete_etemplate_modal').on('submit', '#delete_template_form', function(){

    $.ajax({
      url : $(this).attr('data-href'),
      type : 'POST',
      dataType: 'json',
      success : function(data){
        $('#delete_etemplate_modal').modal('hide');
        location.reload();
      }
    });
  });

  $(document).on('click', '#assign_eprotocol_link', function(){

    $.ajax({
      url : $(this).attr('data-href'),
      type : 'get',
      dataType: 'json',
      beforeSend: function(){
        $('#assign_eprotocol_modal').modal({show : true, backdrop : 'static', keyboard : false});
      },
      success : function(data){
        $('#assign_eprotocol_modal .modal-content').html(data.html_form);
      }
    });

  });

  $('#assign_eprotocol_modal').on('submit', '.assign_eprotocol_form', function(){

      var form = $(this);

      $('#ajax_loader').show();

      $.ajax({

          url : form.attr('data-url'),
          data : form.serialize(),
          type : form.attr('method'),
          dataType : 'json',
          success : function(data){

              $('#ajax_loader').hide();

              if(data.form_is_valid){

                  $('#assign_eprotocol_modal').modal('hide');
                  location.reload();

              }else{

                 $('#assign_eprotocol_modal .modal-content').html(data.html_form);
                 $('#assign_eprotocol_modal .assin_at_least').show();

              }
          }
      });
      return false;
  });

  // to handle edit project
  $('#id_user_eprotocols').on('click', '.update-eprotocol', function(){

        var btn = $(this);
        
        $.ajax({

            url : btn.attr('data-url'),
            type : 'get',
            dataType : 'json',
            beforeSend : function() {
              $('#edit_eprotocol_modal').modal({show : true, backdrop : 'static', keyboard : false});
            },
            success : function(data) {
              $('#edit_eprotocol_modal .modal-content').html(data.html_form);
            }


        });
  });

  $('#edit_eprotocol_modal').on('submit', '.edit_eprotocol_form', function() {

    var form = $(this);

    $('#ajax_loader').show();

    $.ajax({
      url : form.attr('data-url'),
      data : form.serialize(),
      type : form.attr('method'),
      dataType : 'json',
      success : function(data){

          $('#ajax_loader').hide();

          if(data.form_is_valid) {

              $('#edit_eprotocol_modal').modal('hide');
              location.reload();
          }
          else {
            $('#edit_eprotocol_modal .modal-content').html(data.html_form);
             $("select[name=therapeutic_area]").chosen('destroy').chosen();
          }
      }
    });
    return false;
  });

  $('.title_page_article').on('click', '.title_page_sub_btn', function(){

    $('#eprotocol_titlepage_form').submit();

  });

  $(document).on('submit', '.eProtocol_section_form', function(event){

    event.preventDefault();

    var form = $(this);

    $.ajax({

      url : form.attr('data-url'),
      data : form.serialize(),
      type : form.attr('method'),
      dataType : 'json',
      success : function(data){
        location.reload();
      }

    });

  });

  $(document).on('click', '.help_btn', function(){

    $.ajax({

      url : $(this).attr('data-url'),
      method : 'GET',
      dataType: 'json',
      beforeSend: function(){
        $('#section_help_modal').modal({show : true, backdrop : 'static', keyboard : false});
      },
      success: function(data){
        $('#section_help_modal .modal-content').html(data.html_form);
      }

    });

  });

  $(document).on('click', '#saveas_template', function(){

    $.ajax({

      url : $(this).attr('data-href'),
      method : 'GET',
      dataType: 'json',
      beforeSend: function(){
        $('#save_as_temp_modal').modal({show : true, backdrop : 'static', keyboard : false});
      },
      success: function(data){
        $('#save_as_temp_modal .modal-content').html(data.html_form);
      }

    });

  });

  $('#save_as_temp_modal').on('click', '#save_btn_as_template', function(){

    $('.save_as_temp_form').submit();

  });

  $('#save_as_temp_modal').on('submit', '.save_as_temp_form', function(){

    var form = $(this);

    $.ajax({

      url : form.attr('data-url'),
      data : form.serialize(),
      type : form.attr('method'),
      dataType : 'json',
      success : function(data){
        location.reload();
      }

    });

  });


  $(document).on('click', '.template_btn', function(event){

    event.preventDefault();

    $.ajax({

      url : $(this).attr('data-url'),
      method : 'GET',
      dataType: 'json',
      beforeSend: function(){
        $('#section_template_modal').modal({show : true, backdrop : 'static', keyboard : false, 'height':'600px'});
      },
      success: function(data){
        $('#section_template_modal .modal-content').html(data.html_form);
      }

    });

  });

  $(document).on('change', '#section_temp_drodwn', function(){

    var a = $(this).val();

    if(a != ''){

      $.ajax({

        url : a,
        method : 'GET',
        dataType : 'json',
        success: function(data){
          $('#section_template_modal .modal-content .modal-body #template_section_content').html(data.html_form);
          $('.copyToEditor').css("display", "block");
        }

      });

    }else{
      $('#section_template_modal .modal-content .modal-body #template_section_content').html('');
      $('.copyToEditor').css("display", "none");
    }

  });

  $(document).on('click', '.copyToEditor', function(){

    var id = $(this).attr('data-id');

    var text_to_insert  = document.getElementById('template_section_content').innerHTML;

    CKEDITOR.instances['id_sec_content-' + id].insertHtml(text_to_insert)

  });


  $(document).on('keyup change', '.title_page', function(){

    $(this).closest('form').find('input[type="button"]').prop('disabled',false);

  });

  $(document).on('keyup change', '.eProtocol_section_form', function(){

    $(this).closest('form').find('input[type="submit"]').prop('disabled',false);

  });


  $('.tabordion').on('click', 'input[type="radio"]', function(e){

    // e.preventDefault();

    if($('input[type="button"]').prop('disabled') == false){
      $('#unsaved_modal').modal({show : true, backdrop : 'static', keyboard : false});
      return false;
    }
    return true;
    
  });

  $(document).on('click', '.ref_btn', function(){

    $.ajax({
      url : $(this).attr('data-url'),
      method : 'GET',
      dataType: 'json',
      beforeSend: function(){
        $('#reference_modal').modal({show : true, backdrop : 'static', keyboard : false});
      },
      success: function(data){
        $('#reference_modal .modal-content').html(data.html_form);
      }
    });

  });

  $(document).on('click', '#ref_search_btn', function(){

    $('#ajax_loader').show();

    var ref_search_text = $('#ref_search_text').val();

    var prot_id = $('#pro_idd').val();

    var sec_id = $('#sec_idd').val();

    var search_text = JSON.stringify([ref_search_text, prot_id, sec_id]);

    // var search_text = ();

    $.ajax({
      type : 'POST',
      url : $(this).attr('data-url'),
      data : search_text,
      dataType : 'json',
      success: function(data){
        $('#reference_modal .modal-content .modal-body #ref_search_results').empty().html(data.html_form);
        $('#ajax_loader').hide();
      },
    });

  });

  $('#reference_modal').on('hidden.bs.modal', function() {
    $('#ref_search_text').val('');
    $('#reference_modal .modal-content .modal-body #ref_search_results').empty();
  });

  $(document).on('click', '.citation_import_btn', function(){

    var id = $(this).attr('data-id');

    $('#ajax_loader').show();

    $.ajax({
      type : 'GET',
      url : $(this).attr('data-url'),
      dataType : 'json',
      success: function(data){

        var html = "<cite>" + data.ref_count + "</cite>"

        CKEDITOR.instances['id_sec_content-' + id].insertHtml(html)


        $('#reference_modal').modal("hide");
        $('#ajax_loader').hide();
      },
    });

  });



});
