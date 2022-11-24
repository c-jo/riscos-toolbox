
/* to save space we allow compressed draw files */

/* * our redraw routine copes with up to 8 superimposed draw files (this 
 can easily be changed * load_in_file, loads (if necessary decompressing 
 as well) a draw file into a specific layer. */


def load_file(file):
    swi('OS_

int load_in_file(Viewer *view,char * filename,int layer)
{
   if (!*filename) return FAILED;

   view->draw_size[layer] = file_size(filename);
   if ((!(view->draw_size[layer])) || ((view->drawfile[layer] = malloc (4+view->draw_size[layer])) == NULL)) return FAILED;

   if (!file_load(filename,view->drawfile[layer])) {

      if (decompress(&(view->drawfile[layer]),&(view->draw_size[layer])) 
         == FAILED) { free (view->drawfile[layer]); 
         view->drawfile[layer] =0; return FAILED;
      }

      view->files[layer] = filename;

      view->num_draw = layer+1;

      return SUCCESS;
   }
   else return FAILED;
}

/* loads a draw file into the bottom layer */

int draw_file_load(Viewer *view,char * filename)
{
   return load_in_file(view,filename,0);
}

int redraw_window(int event_code, WimpPollBlock *event,IdBlock *id_block,void *v)
{
   int more,height;
   WimpGetWindowStateBlock state;
   WimpRedrawWindowBlock block;
   BBox extent;
   Viewer *view = (Viewer *)v;

   IGNORE(id_block);
   IGNORE(event_code);

   state.window_handle = event->redraw_window_request.window_handle;
   block.window_handle = event->redraw_window_request.window_handle;

   wimp_get_window_state(&state);

   window_get_extent(0,view->window,&extent);
   height = extent.ymax -extent.ymin;

   /* the [2][0] and [2][1] members of the transformation matrix are the coordinates
      of where we want the draw file module to render the data */

   view->trfm [2][0] = (state.visible_area.xmin - state.xscroll) * 256;
   view->trfm [2][1] = (state.visible_area.ymax - height - state.yscroll) * 256;

   wimp_redraw_window(&block,&more);
   while (more)
   {
      int i;

      wimp_set_colour((view->colour)+Wimp_BackgroundColour);
      CLG();

      for (i=0; i<view->num_draw; i++) {
        if (view->drawfile[i])
          drawfile_render (0, view->drawfile[i], view->draw_size[i],
            &(view->trfm), &(block.redraw_area),0);
      }
      wimp_get_rectangle (&block,&more);
   }

   /* claimed */

   return 1;
}

/* loads a draw file into the next available layer */

int do_overlay(Viewer *view,char * filename)
{

   /* can only cope with MAX_LAYERS layers */

   if (view->num_draw == MAX_LAYERS) return FAILED;

   view->draw_size[view->num_draw]=0;
   return load_in_file(view,filename,view->num_draw);
}

void apply_scale (Viewer *v, int factor)
{
   int scale;
   BBox box;

   scale = ((factor) <<16) /100;
   v->trfm[0][0] = scale;
   v->trfm[1][1] = scale;

   box = v->extent;

   box.xmax = (box.xmax * factor) /100;
   box.ymin = (box.ymin * factor) /100;
   window_set_extent(0,v->window,&box);
}

/*
 * the scale object that we use is shared amongst all the viewers. As we have
 * set the 'Ancestor' flag of the viewer window, the object id of the viewer
 * that was menu'd over to give us the scale dialogue is stored in the id block.
 * The drawfile renderer expects a transformation matrix - we simply build this
 * from the supplied scale value percentage.
 */

int scale_view(int event_code, ToolboxEvent  *event, IdBlock *id_block,
                   void  *handle)
{
   ScaleApplyFactorEvent *ev = (ScaleApplyFactorEvent *)event;
   Viewer *v;

   IGNORE(handle);
   IGNORE(event_code);

   toolbox_get_client_handle(0,id_block->ancestor_id,(void **) &v);

   apply_scale (v,ev->factor);

   toolbox_show_object(0,id_block->ancestor_id,Toolbox_ShowObject_Default,0,0,0);
   commands_goto_self(v);

   return 1;

}

static int determine_scale(Viewer *v)
{
   return (((1<<15) + (v->trfm[0][0] *100)) >> 16);
}

int scale_show(int event_code, ToolboxEvent  *event, IdBlock *id_block,
                   void  *handle)
{
   Viewer *v;

   IGNORE(handle);
   IGNORE(event_code);
   IGNORE(event);

   toolbox_get_client_handle(0,id_block->ancestor_id,(void **) &v);

   scale_set_value(0,id_block->self_id,determine_scale(v));

   return 1;
}
