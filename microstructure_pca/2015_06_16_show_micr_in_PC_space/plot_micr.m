function [ ] = plot_micr( M, el )

    M = reshape(M,[el,el,el]);
    
    plt_idx = ceil(el/2);

    image(squeeze(M(plt_idx,:,:)),'CDataMapping','scaled')
    set(gca,'YDir','normal')

    colorbar
    axis equal
    grid on
    axis([0.5 el+0.5 0.5 el+0.5])

end

