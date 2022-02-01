// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xas99r.psi.impl;

import java.util.List;
import org.jetbrains.annotations.*;
import com.intellij.lang.ASTNode;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiElementVisitor;
import com.intellij.psi.util.PsiTreeUtil;
import static net.endlos.xdt99.xas99r.psi.Xas99RTypes.*;
import com.intellij.extapi.psi.ASTWrapperPsiElement;
import net.endlos.xdt99.xas99r.psi.*;

public class Xas99RDirectiveImpl extends ASTWrapperPsiElement implements Xas99RDirective {

  public Xas99RDirectiveImpl(@NotNull ASTNode node) {
    super(node);
  }

  public void accept(@NotNull Xas99RVisitor visitor) {
    visitor.visitDirective(this);
  }

  @Override
  public void accept(@NotNull PsiElementVisitor visitor) {
    if (visitor instanceof Xas99RVisitor) accept((Xas99RVisitor)visitor);
    else super.accept(visitor);
  }

  @Override
  @Nullable
  public Xas99RArgsDirC getArgsDirC() {
    return findChildByClass(Xas99RArgsDirC.class);
  }

  @Override
  @Nullable
  public Xas99RArgsDirE getArgsDirE() {
    return findChildByClass(Xas99RArgsDirE.class);
  }

  @Override
  @Nullable
  public Xas99RArgsDirEO getArgsDirEO() {
    return findChildByClass(Xas99RArgsDirEO.class);
  }

  @Override
  @Nullable
  public Xas99RArgsDirES getArgsDirES() {
    return findChildByClass(Xas99RArgsDirES.class);
  }

  @Override
  @Nullable
  public Xas99RArgsDirF getArgsDirF() {
    return findChildByClass(Xas99RArgsDirF.class);
  }

  @Override
  @Nullable
  public Xas99RArgsDirL getArgsDirL() {
    return findChildByClass(Xas99RArgsDirL.class);
  }

  @Override
  @Nullable
  public Xas99RArgsDirR getArgsDirR() {
    return findChildByClass(Xas99RArgsDirR.class);
  }

  @Override
  @Nullable
  public Xas99RArgsDirS getArgsDirS() {
    return findChildByClass(Xas99RArgsDirS.class);
  }

  @Override
  @Nullable
  public Xas99RArgsDirT getArgsDirT() {
    return findChildByClass(Xas99RArgsDirT.class);
  }

}
