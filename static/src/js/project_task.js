odoo.define('project_trello_design.ProjectTask', function (require) {
'use strict';

    var time = require('web.time');
    var publicWidget = require('web.public.widget');

    publicWidget.registry.ProjectTask = publicWidget.Widget.extend({
        selector: '.project-task-cls',
        events: {
            'click .approve-design': 'approveDesign',
            'click .reject-design': 'rejectDesign',
            'click .submit-detail': 'submitDetail',
            'click .need-print': 'needPrint',
            'click .no-need-print': 'noNeedPrint',
        },
        start: function () {
            var self = this;
            var def = this._super.apply(this, arguments);
            $(".photo_sample").change(function(ev){
                ev.preventDefault();
                $("#photos_sample").empty();
                var image = this.files[0]
                var upload_files = [];
                let fr = new FileReader();
                fr.onload = function () {
                    let data = fr.result;
                    $("#photos_sample").append('<img src="'+data+'" class="img-thumbnail col-sm-6" style="width: 50%;height: 50% !important;max-width: 50% !important;">');
                    let vals = {
                        name: image.name,
                        type: image.type,
                        data : data,
                    };
                    upload_files.push(vals);
                    let img_name = 'img_sample_data';
                    let view = `<textarea  name="`+img_name+`"   class="`+img_name+`" 
                         style="display: none;" >`+JSON.stringify(vals);+`</textarea>`;
                    $('.image_data_div').append(view);
                };
                fr.readAsDataURL(image);
            });
            return def
        },
        approveDesign: function () {
            var task_id = parseInt($(".approve-design").attr('data-id'))
            var logo = parseInt($("#logo:checked").attr('data-id'))
            console.log("========== ", logo)
            var ajax = odoo.__DEBUG__.services['web.ajax'];
            ajax.jsonRpc('/web/dataset/call_kw', 'call', {
                model: 'project.task.type',
                method: 'search',
                args: [[['stage_type','=','approved']]],
                kwargs: {}
            }).then(function(stage) {
                ajax.jsonRpc('/web/dataset/call_kw', 'call', {
                    model: 'project.task',
                    method: 'write',
                    args: [task_id, {'stage_id': stage[0], 'logo': logo}],
                    kwargs: {}
                }).then(function() {
                    $(".approve-design").css({'display':'none'});
                    $(".reject-design").css({'display':'none'});
                    $(".status-task").text("WORK APPROVED");
                    $("#successMessage").css({'display':'inline'});
                    $("#successMessage").delay(2000).slideUp(300);
                    location.reload();
                });
            });
        },
        rejectDesign: function () {
            $('.reject-task').css({"display": "block"});
            $('.approve-click').css({"display": "none"});
        },
        submitDetail: function () {
            var task_id = parseInt($(".submit-detail").attr('data-id'))
            var ajax = require('web.ajax');
            var reject_reason = $("#reject_reason").val()
            var image_data = $('.img_sample_data').val()
            var task_vals = {}
            if(typeof image_data === 'undefined' && !reject_reason){
                $("#rejectionMessage").css({'display':'inline'});
                $("#rejectionMessage").delay(3000).slideUp(300);
                return
            }
            if(typeof image_data !== 'undefined'){
                var revision_image = JSON.parse(image_data)['data'];
                task_vals['revision_image'] = revision_image.split(',')[1]
                var attach_vals = {
                    'name': JSON.parse(image_data)['name'],
                    'type': 'binary',
                    'public': true,
                    'res_model': 'project.task',
                    'res_id' : task_id,
                    'datas': revision_image.split(',')[1],
                }
                ajax.jsonRpc('/web/dataset/call', 'call', {
                    model: 'ir.attachment',
                    method: 'create',
                    args: [
                        attach_vals
                    ],
                    kwargs: {},
                });
            }
            ajax.jsonRpc('/web/dataset/call_kw', 'call', {
                model: 'project.task.type',
                method: 'search',
                args: [[['stage_type','=','revision']]],
                kwargs: {}
            }).then(function(stage) {
                task_vals['stage_id'] = stage[0];
                task_vals['revision_note'] = reject_reason;
                ajax.jsonRpc('/web/dataset/call_kw', 'call', {
                    model: 'project.task',
                    method: 'write',
                    args: [task_id, task_vals],
                    kwargs: {}
                }).then(function() {
                    location.reload();
                });
            });
        },
        needPrint: function () {
            var task_id = parseInt($(".need-print").attr('data-id'))
            // var ajax = odoo.__DEBUG__.services['web.ajax'];
            var ajax = require('web.ajax');
            console.log("======== need print", window.location.origin)
            var url = window.location.origin + "/graphic?task_id=" + task_id
            window.location = url
            // window.location = "http://0.0.0.0:8013/graphic"
            // ajax.jsonRpc("/graphic", 'call', {'task_id': task_id}).then(function() {
            //     console.log("======== graphics")
            // });
            // ajax.jsonRpc('/web/dataset/call_kw', 'call', {
            //     model: 'project.project',
            //     method: 'create',
            //     args: [[['stage_type','=','in_print']]],
            //     kwargs: {}
            // }).then(function(stage) {
            //     ajax.jsonRpc('/web/dataset/call_kw', 'call', {
            //         model: 'project.task',
            //         method: 'write',
            //         args: [task_id, {'stage_id': stage[0]}],
            //         kwargs: {}
            //     }).then(function() {
            //         $(".no-need-print").css({'display':'none'});
            //         $(".need-print").css({'display':'none'});
            //         $(".print-click").css({'display':'none'});
            //         $(".status-task").text("IN PRINT");
            //         $("#successMessage").css({'display':'inline'});
            //         $("#successMessage").delay(2000).slideUp(300);
            //     });
            // });
        },
        noNeedPrint: function () {
            var task_id = parseInt($(".no-need-print").attr('data-id'))
            var ajax = odoo.__DEBUG__.services['web.ajax'];
            ajax.jsonRpc('/web/dataset/call_kw', 'call', {
                model: 'project.task.type',
                method: 'search',
                args: [[['stage_type','=','job_done']]],
                kwargs: {}
            }).then(function(stage) {
                ajax.jsonRpc('/web/dataset/call_kw', 'call', {
                    model: 'project.task',
                    method: 'write',
                    args: [task_id, {'stage_id': stage[0]}],
                    kwargs: {}
                }).then(function() {
                    $(".no-need-print").css({'display':'none'});
                    $(".need-print").css({'display':'none'});
                    $(".print-click").css({'display':'none'});
                    $(".status-task").text("DONE");
                    $("#successMessage").css({'display':'inline'});
                    $("#successMessage").delay(2000).slideUp(300);
                });
            });
        },
    });
});
